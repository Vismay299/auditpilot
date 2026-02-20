"""
Image processing: BLIP captioning + BART zero-shot classification.
"""
import logging
from io import BytesIO
from PIL import Image

from app.services.hf_client import HFInferenceClient

logger = logging.getLogger(__name__)

# Ordered caption model fallback list. Some public models may become unavailable
# on the shared Inference API and return HTTP 410/404.
CAPTION_MODELS = [
    "nlpconnect/vit-gpt2-image-captioning",
    "Salesforce/blip-image-captioning-large",
]

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
        last_error: Exception | None = None

        for model in CAPTION_MODELS:
            try:
                result = await self.hf.inference_binary(model, image_bytes)
                # Common response shape: [{"generated_text": "..."}]
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "")
                    if text:
                        return text
                # Alternate shape: {"generated_text": "..."}
                if isinstance(result, dict):
                    text = result.get("generated_text", "")
                    if text:
                        return text
                logger.warning("Unexpected caption response for model %s: %s", model, type(result))
            except Exception as exc:
                last_error = exc
                logger.warning("Caption model failed (%s): %s", model, exc)

        if last_error:
            raise last_error
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
