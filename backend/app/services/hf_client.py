"""
Async client for the Hugging Face Inference API.
Handles retries, rate‐limiting, and both binary + JSON payloads.
"""
import asyncio
import logging
import os
import time

import httpx

logger = logging.getLogger(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models"
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
MAX_RETRIES = 3
RATE_LIMIT_PER_MIN = 30


class HFInferenceClient:
    """Thin async wrapper around the HF Inference REST API."""

    def __init__(self, token: str | None = None):
        self.token = token or HF_API_TOKEN
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self._client: httpx.AsyncClient | None = None
        # simple sliding‐window rate limiter
        self._call_times: list[float] = []

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=90.0)
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    # ---------- rate limiting ----------

    async def _wait_for_rate_limit(self) -> None:
        """Block until we're below RATE_LIMIT_PER_MIN."""
        now = time.monotonic()
        window = 60.0
        self._call_times = [t for t in self._call_times if now - t < window]
        if len(self._call_times) >= RATE_LIMIT_PER_MIN:
            wait = window - (now - self._call_times[0]) + 0.5
            logger.info("Rate limit reached, waiting %.1fs", wait)
            await asyncio.sleep(wait)

    # ---------- public methods ----------

    async def inference_json(self, model: str, payload: dict) -> dict | list:
        """Send a JSON payload (text tasks like classification, summarization)."""
        return await self._call(model, json_payload=payload)

    async def inference_binary(self, model: str, data: bytes) -> dict | list:
        """Send raw bytes (images, audio)."""
        return await self._call(model, binary_payload=data)

    # ---------- internal ----------

    async def _call(
        self,
        model: str,
        json_payload: dict | None = None,
        binary_payload: bytes | None = None,
    ) -> dict | list:
        url = f"{HF_API_URL}/{model}"
        client = await self._get_client()

        for attempt in range(1, MAX_RETRIES + 1):
            await self._wait_for_rate_limit()
            self._call_times.append(time.monotonic())

            try:
                if binary_payload is not None:
                    resp = await client.post(
                        url,
                        headers=self.headers,
                        content=binary_payload,
                    )
                else:
                    resp = await client.post(
                        url,
                        headers=self.headers,
                        json=json_payload,
                    )

                # Model is loading — HF returns 503 with estimated_time
                if resp.status_code == 503:
                    body = resp.json()
                    wait = body.get("estimated_time", 20)
                    logger.info("Model %s loading, retrying in %.0fs (attempt %d)", model, wait, attempt)
                    await asyncio.sleep(min(wait, 60))
                    continue

                resp.raise_for_status()
                return resp.json()

            except httpx.HTTPStatusError as exc:
                if attempt < MAX_RETRIES:
                    backoff = 2 ** attempt
                    logger.warning(
                        "HF API error %s for %s, retrying in %ds (attempt %d)",
                        exc.response.status_code, model, backoff, attempt,
                    )
                    await asyncio.sleep(backoff)
                else:
                    logger.error("HF API call failed after %d attempts: %s", MAX_RETRIES, exc)
                    raise
            except httpx.RequestError as exc:
                if attempt < MAX_RETRIES:
                    backoff = 2 ** attempt
                    logger.warning("Request error for %s: %s, retrying in %ds", model, exc, backoff)
                    await asyncio.sleep(backoff)
                else:
                    raise

        raise RuntimeError(f"HF inference failed for {model} after {MAX_RETRIES} retries")
