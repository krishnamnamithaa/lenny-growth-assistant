import uuid
from typing import Optional, List
from sqlalchemy import String, Text, JSON, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from pgvector.sqlalchemy import Vector
from app.models.base import Base

class TranscriptModel(Base):
    __tablename__ = "transcripts"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    guest: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    transcript_type: Mapped[str] = mapped_column(String(50), default="podcast", nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    extra_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    chunks: Mapped[List["TranscriptChunkModel"]] = relationship(
        "TranscriptChunkModel",
        back_populates="transcript",
        cascade="all, delete-orphan",
        order_by="TranscriptChunkModel.chunk_index"
    )

class TranscriptChunkModel(Base):
    __tablename__ = "transcript_chunks"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    transcript_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("transcripts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(384), nullable=True)
    start_char: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    end_char: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    chunk_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    transcript: Mapped["TranscriptModel"] = relationship("TranscriptModel", back_populates="chunks")
