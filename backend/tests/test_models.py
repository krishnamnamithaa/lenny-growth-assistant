import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, SessionModel, MessageModel, TranscriptModel, TranscriptChunkModel
from app.schemas import SessionCreate, SessionResponse, MessageCreate, MessageResponse

# Use in-memory SQLite database for testing models
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

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

def test_session_creation(db_session):
    session_obj = SessionModel(title="Growth Strategy Chat", user_metadata={"device": "desktop"})
    db_session.add(session_obj)
    db_session.commit()
    db_session.refresh(session_obj)

    assert session_obj.id is not None
    assert session_obj.title == "Growth Strategy Chat"
    assert session_obj.user_metadata == {"device": "desktop"}
    assert session_obj.created_at is not None

def test_message_creation_and_session_relationship(db_session):
    session_obj = SessionModel(title="RAG Chat")
    db_session.add(session_obj)
    db_session.commit()

    msg1 = MessageModel(
        session_id=session_obj.id,
        role="user",
        content="What is product market fit?"
    )
    msg2 = MessageModel(
        session_id=session_obj.id,
        role="assistant",
        content="Product market fit is when...",
        sources=[{"title": "Marc Andreessen Episode", "snippet": "PMF definition..."}]
    )
    db_session.add_all([msg1, msg2])
    db_session.commit()

    db_session.refresh(session_obj)
    assert len(session_obj.messages) == 2
    assert session_obj.messages[0].role == "user"
    assert session_obj.messages[1].role == "assistant"
    assert len(session_obj.messages[1].sources) == 1

def test_session_isolation(db_session):
    session1 = SessionModel(title="Session 1")
    session2 = SessionModel(title="Session 2")
    db_session.add_all([session1, session2])
    db_session.commit()

    msg1 = MessageModel(session_id=session1.id, role="user", content="Hello session 1")
    msg2 = MessageModel(session_id=session2.id, role="user", content="Hello session 2")
    db_session.add_all([msg1, msg2])
    db_session.commit()

    db_session.refresh(session1)
    db_session.refresh(session2)

    assert len(session1.messages) == 1
    assert session1.messages[0].content == "Hello session 1"
    assert len(session2.messages) == 1
    assert session2.messages[0].content == "Hello session 2"

def test_cascading_delete(db_session):
    session_obj = SessionModel(title="Temporary Session")
    db_session.add(session_obj)
    db_session.commit()

    msg = MessageModel(session_id=session_obj.id, role="user", content="Will be deleted")
    db_session.add(msg)
    db_session.commit()

    # Delete session
    db_session.delete(session_obj)
    db_session.commit()

    # Verify messages are cascaded deleted
    remaining_messages = db_session.query(MessageModel).filter_by(session_id=session_obj.id).all()
    assert len(remaining_messages) == 0

def test_transcript_and_chunks(db_session):
    transcript = TranscriptModel(
        title="Brian Chesky on Building Airbnb",
        guest="Brian Chesky",
        url="https://lenny.com/chesky",
        transcript_type="podcast",
        raw_content="Full transcript text here..."
    )
    db_session.add(transcript)
    db_session.commit()

    chunk1 = TranscriptChunkModel(
        transcript_id=transcript.id,
        chunk_index=0,
        content="First chunk text...",
        chunk_metadata={"speaker": "Brian Chesky"}
    )
    chunk2 = TranscriptChunkModel(
        transcript_id=transcript.id,
        chunk_index=1,
        content="Second chunk text...",
        chunk_metadata={"speaker": "Lenny Rachitsky"}
    )
    db_session.add_all([chunk1, chunk2])
    db_session.commit()

    db_session.refresh(transcript)
    assert len(transcript.chunks) == 2
    assert transcript.chunks[0].chunk_metadata["speaker"] == "Brian Chesky"
