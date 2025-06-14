from pydantic import BaseModel
from typing import Optional

class DatasetBase(BaseModel):
    name: str
    source_type: str
    table_name: str

class DatasetCreate(DatasetBase):
    pass

class DatasetResponse(DatasetBase):
    id: int

    class Config:
        from_attributes = True