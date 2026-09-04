from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any

class SessionBase(BaseModel):
    title: str = "New Chat"
    user_metadata: Optional[Dict[str, Any]] = None

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    title: Optional[str] = None
    user_metadata: Optional[Dict[str, Any]] = None

class SessionResponse(SessionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
