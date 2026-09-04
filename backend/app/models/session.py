import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.message import MessageModel

class SessionModel(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(255), default="New Chat", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    user_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)

    # Relationships
    messages: Mapped[List["MessageModel"]] = relationship(
        "MessageModel",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="MessageModel.created_at"
    )
