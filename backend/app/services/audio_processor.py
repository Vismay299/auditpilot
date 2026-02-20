"""
Audio processing: Whisper transcription + BART classification.
"""
import logging

from app.services.hf_client import HFInferenceClient
from app.services.image_processor import (
    DEFECT_CATEGORIES,
    CATEGORY_SEVERITY,
    CONFIDENCE_THRESHOLD,
)

logger = logging.getLogger(__name__)


class AudioProcessor:
    def __init__(self, hf: HFInferenceClient):
        self.hf = hf

    async def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio using Whisper."""
        result = await self.hf.inference_binary(
            "openai/whisper-large-v3",
            audio_bytes,
        )
        # result: {"text": "..."} or [{"text": "..."}]
        if isinstance(result, dict):
            return result.get("text", "")
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("text", "")
        return ""

    async def classify_transcription(self, text: str) -> dict:
        """Classify transcription text into defect categories."""
        if not text or len(text.strip()) < 10:
            return {
                "category": "clear/no defect",
                "confidence": 0.0,
                "severity": "clear",
                "needs_review": True,
                "all_scores": {},
            }

        result = await self.hf.inference_json(
            "facebook/bart-large-mnli",
            {
                "inputs": text[:1024],  # truncate to avoid token limits
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
