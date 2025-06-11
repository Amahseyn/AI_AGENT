from pydantic import BaseModel
from typing import List

class MetadataItem(BaseModel):
    source_type: str
    source_name: str
    column_name: str
    column_order: int

    class Config:
        from_attributes = True

class MetadataResponse(BaseModel):
    metadata: List[MetadataItem]