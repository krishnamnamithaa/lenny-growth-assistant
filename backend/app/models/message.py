import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.session import SessionModel

class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False) # 'user', 'assistant', 'system'
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sources: Mapped[Optional[List[dict]]] = mapped_column(JSON, nullable=True, default=list)
    artifact: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="messages")
