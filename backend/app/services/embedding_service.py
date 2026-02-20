"""
Embedding generation via sentence-transformers for pgvector.
"""
import logging
from app.services.hf_client import HFInferenceClient

logger = logging.getLogger(__name__)

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


class EmbeddingService:
    def __init__(self, hf: HFInferenceClient):
        self.hf = hf

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate a 384-dim embedding from text."""
        if not text or not text.strip():
            return [0.0] * EMBEDDING_DIM

        # Truncate very long text (model max ~256 tokens)
        truncated = text[:2000]

        result = await self.hf.inference_json(
            MODEL,
            {"inputs": truncated},
        )

        # HF returns a flat list of floats or a nested list
        if isinstance(result, list):
            if isinstance(result[0], list):
                embedding = result[0]
            else:
                embedding = result
        else:
            logger.warning("Unexpected embedding response: %s", type(result))
            return [0.0] * EMBEDDING_DIM

        if len(embedding) != EMBEDDING_DIM:
            logger.warning("Embedding dim %d != expected %d", len(embedding), EMBEDDING_DIM)

        return embedding
