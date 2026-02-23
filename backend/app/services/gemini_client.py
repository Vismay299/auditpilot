"""
Async client for Google Gemini Vision API (free tier).
Directly analyzes images for building/safety defects.
"""
import base64
import json
import logging
import os
import re

import httpx

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_FALLBACK_MODEL = "gemini-2.0-flash-lite"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
MAX_RETRIES = 3

# Structured prompt for defect analysis
ANALYSIS_PROMPT = """You are an expert building inspector and safety auditor. Analyze this image and identify any defects, hazards, or issues.

You MUST respond with ONLY a valid JSON object (no markdown, no code fences) in this exact format:
{
  "category": "<one of: structural damage, electrical hazard, water damage, fire risk, equipment issue, fall hazard, clear/no defect>",
  "confidence": <float between 0.0 and 1.0>,
  "severity": "<one of: critical, high, medium, low, clear>",
  "description": "<detailed description of what you see, max 2 sentences>",
  "defects_found": <true or false>
}

Category and severity mapping:
- structural damage → critical
- electrical hazard → critical
- fire risk → high
- water damage → high
- fall hazard → high
- equipment issue → medium
- clear/no defect → clear

Rules:
- If you see ANY damage, defect, or hazard, classify it into the most appropriate category. Do NOT default to "clear/no defect".
- Set confidence based on how certain you are about the classification (0.0 = uncertain, 1.0 = very certain).
- Be specific in the description about what you observe.
- If there are multiple issues, report the most severe one.
"""


class GeminiVisionClient:
    """Async client for Google Gemini Vision API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or GEMINI_API_KEY
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=60.0)
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def analyze_image(self, image_bytes: bytes) -> dict:
        """
        Send an image to Gemini Vision for defect analysis.
        Returns a dict with category, confidence, severity, description, needs_review.
        Retries on rate limits (429) and server errors (503) with exponential backoff.
        """
        import asyncio

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Get a free key at https://aistudio.google.com/apikey")

        client = await self._get_client()
        b64_image = base64.b64encode(image_bytes).decode("utf-8")

        # Detect MIME type from image bytes
        mime_type = _detect_mime(image_bytes)

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": ANALYSIS_PROMPT},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": b64_image,
                            }
                        },
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 500,
            },
        }

        # Try primary model, then fallback
        models = [GEMINI_MODEL, GEMINI_FALLBACK_MODEL]
        last_error = None

        for model in models:
            url = f"{GEMINI_BASE_URL}/{model}:generateContent?key={self.api_key}"

            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    resp = await client.post(url, json=payload)

                    # Rate limit — wait and retry
                    if resp.status_code == 429:
                        retry_delay = min(2 ** attempt * 5, 60)  # 10s, 20s, 40s
                        body = resp.json()
                        # Try to extract suggested retry delay
                        details = body.get("error", {}).get("details", [])
                        for d in details:
                            if d.get("@type", "").endswith("RetryInfo"):
                                suggested = d.get("retryDelay", "")
                                if suggested and suggested.endswith("s"):
                                    retry_delay = min(float(suggested.rstrip("s")) + 1, 60)
                        logger.warning("Gemini rate limit (429) for %s, retrying in %.0fs (attempt %d)", model, retry_delay, attempt)
                        await asyncio.sleep(retry_delay)
                        continue

                    # Server error — retry
                    if resp.status_code == 503:
                        backoff = 2 ** attempt
                        logger.warning("Gemini server error (503) for %s, retrying in %ds (attempt %d)", model, backoff, attempt)
                        await asyncio.sleep(backoff)
                        continue

                    resp.raise_for_status()
                    result = resp.json()

                    # Parse Gemini response
                    text = (
                        result.get("candidates", [{}])[0]
                        .get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", "")
                    )

                    parsed = _parse_gemini_response(text)
                    logger.info("Gemini analysis successful with model %s", model)
                    return parsed

                except httpx.HTTPStatusError as exc:
                    last_error = exc
                    if attempt < MAX_RETRIES:
                        backoff = 2 ** attempt
                        logger.warning("Gemini HTTP error %s for %s, retrying in %ds", exc.response.status_code, model, backoff)
                        await asyncio.sleep(backoff)
                    else:
                        logger.error("Gemini failed after %d attempts with model %s: %s", MAX_RETRIES, model, exc)
                        break  # try next model
                except httpx.RequestError as exc:
                    last_error = exc
                    if attempt < MAX_RETRIES:
                        backoff = 2 ** attempt
                        logger.warning("Gemini request error for %s: %s, retrying in %ds", model, exc, backoff)
                        await asyncio.sleep(backoff)
                    else:
                        logger.error("Gemini request failed after %d attempts with model %s: %s", MAX_RETRIES, model, exc)
                        break  # try next model

        raise RuntimeError(f"Gemini Vision analysis failed after all retries: {last_error}")


def _detect_mime(image_bytes: bytes) -> str:
    """Detect image MIME type from magic bytes."""
    if image_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if image_bytes[:2] == b"\xff\xd8":
        return "image/jpeg"
    if image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
        return "image/webp"
    return "image/jpeg"  # default


def _parse_gemini_response(text: str) -> dict:
    """Parse Gemini's JSON response into a structured classification dict."""
    from app.services.image_processor import CATEGORY_SEVERITY, CONFIDENCE_THRESHOLD

    # Strip markdown code fences if present
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("Failed to parse Gemini response as JSON: %s", text[:200])
        return {
            "category": "unknown",
            "confidence": 0.0,
            "severity": "medium",
            "needs_review": True,
            "description": f"AI analysis returned unparseable response. Raw: {text[:200]}",
            "all_scores": {},
        }

    category = data.get("category", "unknown").lower()
    confidence = float(data.get("confidence", 0.0))
    severity = data.get("severity", CATEGORY_SEVERITY.get(category, "medium"))
    description = data.get("description", "")

    return {
        "category": category,
        "confidence": confidence,
        "severity": severity,
        "needs_review": confidence < CONFIDENCE_THRESHOLD,
        "description": description,
        "all_scores": {category: confidence},
    }
