import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, TranscriptModel, TranscriptChunkModel
from app.rag.ingestion import (
    validate_transcript_record,
    TranscriptValidationError,
    ingest_transcript_data,
    run_ingestion_pipeline
)
from tests.test_embeddings import MockEmbeddingProvider

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(autouse=True)
def mock_embedding_provider_fixture(monkeypatch):
    monkeypatch.setattr("app.rag.ingestion.get_embedding_provider", lambda: MockEmbeddingProvider())

@pytest.fixture
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_validate_transcript_record_valid():
    data = {
        "title": "Brian Chesky on Airbnb",
        "content": "Lenny: Welcome Brian.\nBrian: Thanks Lenny.",
        "speaker": "Brian Chesky",
        "source_url": "https://lenny.com/chesky"
    }
    val = validate_transcript_record(data)
    assert val["title"] == "Brian Chesky on Airbnb"
    assert val["content"] == "Lenny: Welcome Brian.\nBrian: Thanks Lenny."
    assert val["speaker"] == "Brian Chesky"

def test_validate_transcript_record_missing_title():
    with pytest.raises(TranscriptValidationError, match="title"):
        validate_transcript_record({"content": "Text without title"})

def test_validate_transcript_record_missing_content():
    with pytest.raises(TranscriptValidationError, match="content"):
        validate_transcript_record({"title": "Title without content"})

def test_ingest_transcript_data_single(db_session):
    mock_provider = MockEmbeddingProvider()
    val_data = {
        "title": "Shreyas Doshi Episode",
        "content": "Lenny: Welcome Shreyas.\nShreyas: The LNO framework is Leverage, Neutral, Overhead.",
        "speaker": "Shreyas Doshi",
        "source_url": "https://lenny.com/shreyas",
        "published_at": "2022-06-05",
        "description": "Episode description"
    }
    res = ingest_transcript_data(db_session, val_data, mock_provider, chunk_size=300)
    assert res["transcript_id"] is not None
    assert res["chunks_created"] >= 1

    # Verify database persistence
    t_obj = db_session.query(TranscriptModel).filter_by(id=res["transcript_id"]).first()
    assert t_obj is not None
    assert t_obj.title == "Shreyas Doshi Episode"
    assert len(t_obj.chunks) == res["chunks_created"]

def test_ingest_transcript_deduplication_and_update(db_session):
    mock_provider = MockEmbeddingProvider()
    val_data_v1 = {
        "title": "Elena Verna Episode",
        "content": "Lenny: Welcome Elena.\nElena: Activation is key.",
        "speaker": "Elena Verna",
        "source_url": "https://lenny.com/elena"
    }
    res1 = ingest_transcript_data(db_session, val_data_v1, mock_provider)
    initial_chunks = res1["chunks_created"]

    # Re-ingest updated content for same URL
    val_data_v2 = {
        "title": "Elena Verna Episode - Updated",
        "content": "Lenny: Welcome Elena.\nElena: Activation is key. Growth loops drive viral retention.",
        "speaker": "Elena Verna",
        "source_url": "https://lenny.com/elena"
    }
    res2 = ingest_transcript_data(db_session, val_data_v2, mock_provider)

    # Verify transcript updated instead of creating duplicate
    all_transcripts = db_session.query(TranscriptModel).filter_by(url="https://lenny.com/elena").all()
    assert len(all_transcripts) == 1
    assert all_transcripts[0].title == "Elena Verna Episode - Updated"
    
    # Verify stale chunks replaced
    all_chunks = db_session.query(TranscriptChunkModel).filter_by(transcript_id=all_transcripts[0].id).all()
    assert len(all_chunks) == res2["chunks_created"]
