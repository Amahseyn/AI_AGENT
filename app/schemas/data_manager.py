from pydantic import BaseModel
from typing import Dict, Optional, List

class FieldMapping(BaseModel):
    mappings: Dict[str, str] = {}     # {"source_col": "target_field"}
    skip_columns: Optional[List[str]] = []

class RecordUpdate(BaseModel):
    updates: Dict[str, str]