# app/api/v1/routes/schema_extractor.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.schemas.schema_extractor import MetadataResponse
from app.crud.schema_extractor import process_uploaded_file, scan_database
from app.dependencies import get_current_user, get_db
import os 

router = APIRouter(prefix="/schema", tags=["Schema Extractor"])


SUPPORTED_EXTENSIONS = ('.csv', '.xls', '.xlsx', '.json')

@router.post("/upload-file/", response_model=MetadataResponse)
def extract_metadata_from_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Get file extension
    _, ext = os.path.splitext(file.filename)

    if ext.lower() not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Supported types: {SUPPORTED_EXTENSIONS}"
        )

    return {"metadata": process_uploaded_file(file)}


@router.post("/scan-database/", response_model=MetadataResponse)
def extract_metadata_from_database(
    db_url: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Scan a database and extract table/column metadata.
    Supported DBs: SQLite, PostgreSQL, MySQL.
    Only authenticated users can use this endpoint.
    """
    if not db_url.startswith(("sqlite://", "postgresql://", "mysql://")):
        raise HTTPException(status_code=400, detail="Invalid or unsupported DB URL")
    
    return {"metadata": scan_database(db_url)}