from pydantic import BaseModel
from datetime import datetime
from typing import List

class SessionBase(BaseModel):
    name: str

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True