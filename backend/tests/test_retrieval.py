import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.models import Base, TranscriptModel, TranscriptChunkModel
from app.rag.retrieval import retrieve_relevant_chunks
from app.db import get_db
from tests.test_embeddings import MockEmbeddingProvider

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def mock_embedding_provider(monkeypatch):
    monkeypatch.setattr("app.rag.retrieval.get_embedding_provider", lambda: MockEmbeddingProvider())

@pytest.fixture
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()

def test_retrieve_empty_query(db_session):
    mock_provider = MockEmbeddingProvider()
    results = retrieve_relevant_chunks("", top_k=5, db=db_session, embedding_provider=mock_provider)
    assert results == []

def test_retrieve_empty_database(db_session):
    mock_provider = MockEmbeddingProvider()
    results = retrieve_relevant_chunks("How to scale PLG?", top_k=5, db=db_session, embedding_provider=mock_provider)
    assert results == []

def test_retrieve_with_data(db_session):
    mock_provider = MockEmbeddingProvider()
    transcript = TranscriptModel(
        title="Elena Verna on PLG",
        guest="Elena Verna",
        url="https://lenny.com/elena",
        raw_content="Activation is key."
    )
    db_session.add(transcript)
    db_session.commit()

    chunk = TranscriptChunkModel(
        transcript_id=transcript.id,
        chunk_index=0,
        content="Activation is the moment user experiences core value.",
        embedding=[0.1] * 384,
        chunk_metadata={"speaker": "Elena Verna"}
    )
    db_session.add(chunk)
    db_session.commit()

    results = retrieve_relevant_chunks("activation", top_k=5, min_similarity=0.0, db=db_session, embedding_provider=mock_provider)
    assert len(results) == 1
    item = results[0]
    assert item["title"] == "Elena Verna on PLG"
    assert item["speaker"] == "Elena Verna"
    assert item["source_url"] == "https://lenny.com/elena"
    assert "activation" in item["content"].lower()
    assert "similarity" in item

def test_retrieval_api_endpoint_success(client, db_session):
    # Seed transcript and chunk
    transcript = TranscriptModel(
        title="Shreyas Doshi Episode",
        guest="Shreyas Doshi",
        url="https://lenny.com/shreyas",
        raw_content="LNO framework."
    )
    db_session.add(transcript)
    db_session.commit()

    chunk = TranscriptChunkModel(
        transcript_id=transcript.id,
        chunk_index=0,
        content="LNO framework stands for Leverage, Neutral, Overhead.",
        embedding=[0.1] * 384
    )
    db_session.add(chunk)
    db_session.commit()

    payload = {"query": "What is the LNO framework?", "top_k": 3, "min_similarity": 0.0}
    response = client.post("/retrieval/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "What is the LNO framework?"
    assert data["results_count"] == 1
    assert data["results"][0]["title"] == "Shreyas Doshi Episode"

def test_retrieval_api_endpoint_empty_query(client):
    response = client.post("/retrieval/search", json={"query": "   ", "top_k": 5})
    assert response.status_code == 422 # Validation error for empty query

def test_retrieval_api_endpoint_invalid_top_k(client):
    response = client.post("/retrieval/search", json={"query": "growth", "top_k": 50})
    assert response.status_code == 422 # top_k > 20 validation error
