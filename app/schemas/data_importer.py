from pydantic import BaseModel
from typing import List, Dict, Optional


class ColumnPreviewResponse(BaseModel):
    columns: List[str]


class ColumnMappingRequest(BaseModel):
    mappings: Dict[str, str] = {}     # {"source_col": "target_field"}
    skip_columns: Optional[List[str]] = []