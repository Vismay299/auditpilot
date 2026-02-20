"""
Image processing: BLIP captioning + BART zero-shot classification.
"""
import logging
from io import BytesIO
from PIL import Image

from app.services.hf_client import HFInferenceClient

logger = logging.getLogger(__name__)

# Defect categories for zero-shot classification
DEFECT_CATEGORIES = [
    "structural damage",
    "electrical hazard",
    "water damage",
    "fire risk",
    "equipment issue",
    "fall hazard",
    "clear/no defect",
]

# Map category → severity
CATEGORY_SEVERITY: dict[str, str] = {
    "structural damage": "critical",
    "electrical hazard": "critical",
    "fire risk": "high",
    "water damage": "high",
    "fall hazard": "high",
    "equipment issue": "medium",
    "clear/no defect": "clear",
}

# confidence threshold – below this the finding needs human review
CONFIDENCE_THRESHOLD = 0.65


class ImageProcessor:
    def __init__(self, hf: HFInferenceClient):
        self.hf = hf

    async def generate_caption(self, image_bytes: bytes) -> str:
        """Generate a text caption using BLIP."""
        # Resize large images to < 2 MB for HF API
        image_bytes = _resize_if_needed(image_bytes, max_bytes=2 * 1024 * 1024)

        result = await self.hf.inference_binary(
            "Salesforce/blip-image-captioning-large",
            image_bytes,
        )
        # result is a list: [{"generated_text": "..."}]
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        return ""

    async def classify_text(self, text: str) -> dict:
        """Zero-shot classify text into defect categories using BART-MNLI."""
        result = await self.hf.inference_json(
            "facebook/bart-large-mnli",
            {
                "inputs": text,
                "parameters": {"candidate_labels": DEFECT_CATEGORIES},
            },
        )
        # result: {"labels": [...], "scores": [...], "sequence": "..."}
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


def _resize_if_needed(image_bytes: bytes, max_bytes: int = 2 * 1024 * 1024) -> bytes:
    """Resize image if larger than max_bytes."""
    if len(image_bytes) <= max_bytes:
        return image_bytes

    img = Image.open(BytesIO(image_bytes))
    # reduce by 50% until under limit
    quality = 85
    while len(image_bytes) > max_bytes and quality > 20:
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        image_bytes = buf.getvalue()
        quality -= 15

    logger.info("Resized image to %d bytes (quality=%d)", len(image_bytes), quality + 15)
    return image_bytes
