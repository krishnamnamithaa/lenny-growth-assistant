from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any

class TranscriptChunkResponse(BaseModel):
    id: str
    transcript_id: str
    chunk_index: int
    content: str
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    chunk_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TranscriptBase(BaseModel):
    title: str
    guest: Optional[str] = None
    url: Optional[str] = None
    transcript_type: str = "podcast"
    extra_metadata: Optional[Dict[str, Any]] = None

class TranscriptCreate(TranscriptBase):
    raw_content: str

class TranscriptResponse(TranscriptBase):
    id: str
    created_at: datetime
    chunk_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
