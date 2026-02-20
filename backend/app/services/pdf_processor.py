"""
PDF processing: text extraction via pypdf + BART classification.
"""
import logging
from io import BytesIO

from pypdf import PdfReader

from app.services.hf_client import HFInferenceClient
from app.services.image_processor import (
    DEFECT_CATEGORIES,
    CATEGORY_SEVERITY,
    CONFIDENCE_THRESHOLD,
)

logger = logging.getLogger(__name__)


class PdfProcessor:
    def __init__(self, hf: HFInferenceClient):
        self.hf = hf

    async def extract_text(self, pdf_bytes: bytes) -> str:
        """Extract all text from a PDF using pypdf (no API call needed)."""
        reader = PdfReader(BytesIO(pdf_bytes))
        pages: list[str] = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
        full_text = "\n\n".join(pages)
        logger.info("Extracted %d chars from %d pages", len(full_text), len(reader.pages))
        return full_text

    async def classify_text(self, text: str) -> dict:
        """Classify extracted text into defect categories."""
        if not text or len(text.strip()) < 10:
            return {
                "category": "clear/no defect",
                "confidence": 0.0,
                "severity": "clear",
                "needs_review": True,
                "all_scores": {},
            }

        # Use first 1024 chars for classification (BART token limit)
        result = await self.hf.inference_json(
            "facebook/bart-large-mnli",
            {
                "inputs": text[:1024],
                "parameters": {"candidate_labels": DEFECT_CATEGORIES},
            },
        )
        labels = result.get("labels", DEFECT_CATEGORIES)
        scores = result.get("scores", [0.0] * len(DEFECT_CATEGORIES))
        top_label = labels[0]
        top_score = scores[0]

        return {
            "category": top_label,
            "confidence": top_score,
            "severity": CATEGORY_SEVERITY.get(top_label, "medium"),
            "needs_review": top_score < CONFIDENCE_THRESHOLD,
            "all_scores": dict(zip(labels, scores)),
        }
