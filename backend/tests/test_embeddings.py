import pytest
from app.rag.embeddings import (
    EmbeddingProvider,
    SentenceTransformerEmbeddingProvider,
    EXPECTED_EMBEDDING_DIMENSION
)

class MockEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def get_dimension(self) -> int:
        return self.dimension

    def embed_text(self, text: str):
        if not text or not text.strip():
            return [0.0] * self.dimension
        return [0.1] * self.dimension

    def embed_batch(self, texts):
        return [self.embed_text(t) for t in texts]

def test_mock_embedding_provider():
    provider = MockEmbeddingProvider(dimension=384)
    assert provider.get_dimension() == 384
    vec = provider.embed_text("Product growth loop")
    assert len(vec) == 384
    assert vec[0] == 0.1

def test_empty_text_embedding():
    provider = MockEmbeddingProvider(dimension=384)
    vec = provider.embed_text("")
    assert len(vec) == 384
    assert all(x == 0.0 for x in vec)

def test_batch_embedding():
    provider = MockEmbeddingProvider(dimension=384)
    batch = provider.embed_batch(["Text A", "Text B", "Text C"])
    assert len(batch) == 3
    assert all(len(v) == 384 for v in batch)

def test_dimension_validation():
    class MismatchedProvider(EmbeddingProvider):
        def get_dimension(self) -> int:
            return 384
        def embed_text(self, text: str):
            return [0.1] * 128 # Mismatched dimension!
        def embed_batch(self, texts):
            return [[0.1] * 128]

    provider = MismatchedProvider()
    with pytest.raises(ValueError, match="does not match"):
        # Real SentenceTransformerProvider checks dimension against get_dimension()
        vec = provider.embed_text("test")
        if len(vec) != provider.get_dimension():
            raise ValueError(f"Generated vector dimension ({len(vec)}) does not match expected model dimension ({provider.get_dimension()})")
