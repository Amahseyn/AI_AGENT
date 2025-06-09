from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    session_id: int

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True