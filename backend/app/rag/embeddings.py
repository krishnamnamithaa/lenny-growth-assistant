import logging
from abc import ABC, abstractmethod
from typing import List
from app.config import settings

logger = logging.getLogger(__name__)

EXPECTED_EMBEDDING_DIMENSION = 384

class EmbeddingProvider(ABC):
    """Abstract interface for text embedding providers."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string into a vector float list."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of text strings into vector float lists."""
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """Return vector dimension produced by model."""
        pass

class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    """Local Sentence Transformers embedding provider (default: all-MiniLM-L6-v2)."""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or getattr(settings, "EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
        self._model = None
        self._dimension = EXPECTED_EMBEDDING_DIMENSION

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading SentenceTransformer model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
                sample_vec = self._model.encode("test", convert_to_numpy=True).tolist()
                self._dimension = len(sample_vec)
                logger.info(f"Loaded embedding model {self.model_name} with dimension {self._dimension}")
            except Exception as e:
                logger.error(f"Failed to load SentenceTransformer model {self.model_name}: {e}")
                raise RuntimeError(f"Embedding model initialization failed: {e}")

    def get_dimension(self) -> int:
        if self._model is None:
            self._load_model()
        return self._dimension

    def embed_text(self, text: str) -> List[float]:
        if not text or not text.strip():
            # Return zero vector for empty text
            return [0.0] * self.get_dimension()
            
        self._load_model()
        vector = self._model.encode(text, convert_to_numpy=True).tolist()
        
        # Programmatic dimension validation
        if len(vector) != self.get_dimension():
            raise ValueError(
                f"Generated vector dimension ({len(vector)}) does not match expected model dimension ({self.get_dimension()})"
            )
        return vector

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
            
        self._load_model()
        # Clean texts for embedding
        cleaned_texts = [t if t and t.strip() else " " for t in texts]
        vectors = self._model.encode(cleaned_texts, convert_to_numpy=True, batch_size=32).tolist()
        
        # Dimension validation for all items
        expected_dim = self.get_dimension()
        for idx, vec in enumerate(vectors):
            if len(vec) != expected_dim:
                raise ValueError(
                    f"Generated vector at index {idx} dimension ({len(vec)}) does not match model dimension ({expected_dim})"
                )
        return vectors

def get_embedding_provider() -> EmbeddingProvider:
    """Factory function returning active embedding provider."""
    return SentenceTransformerEmbeddingProvider()
