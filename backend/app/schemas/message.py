from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any

class MessageSource(BaseModel):
    transcript_id: str
    chunk_id: str
    title: str
    guest: Optional[str] = None
    similarity_score: Optional[float] = None
    snippet: str
    url: Optional[str] = None

class ArtifactPayload(BaseModel):
    artifact_type: str # 'markdown' or 'html'
    title: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class MessageBase(BaseModel):
    role: str # 'user', 'assistant', 'system'
    content: str

class MessageCreate(MessageBase):
    session_id: str
    sources: Optional[List[Dict[str, Any]]] = None
    artifact: Optional[Dict[str, Any]] = None

class MessageResponse(MessageBase):
    id: str
    session_id: str
    sources: Optional[List[Dict[str, Any]]] = None
    artifact: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
