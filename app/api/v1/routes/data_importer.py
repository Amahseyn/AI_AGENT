from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.schemas.data_importer import ColumnMappingRequest, ColumnPreviewResponse
from app.schemas.data_manager import FieldMapping
from app.schemas.imported_data import DatasetResponse
from app.crud.data_importer import import_dataset_from_file, import_dataset_from_database, preview_db_columns, preview_file_columns
from app.database.session import get_db
from app.dependencies import get_current_user


router = APIRouter(prefix="/import")


@router.post("/file/", response_model=DatasetResponse)
def import_from_file(
    file: UploadFile = File(...),
    name: str = "Uploaded Dataset",
    table_name: str = "custom_data",
    mappings: FieldMapping = Depends(),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        with open(f"/tmp/{file.filename}", "wb") as f:
            f.write(file.file.read())
        return import_dataset_from_file(
            db,
            f"/tmp/{file.filename}",
            name,
            table_name,
            owner_id=current_user.id,
            mappings=mappings.mappings,
            skip_columns=mappings.skip_columns
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/database/", response_model=DatasetResponse)
def import_from_database(
    db_url: str,
    src_table: str,
    name: str = "Database Dataset",
    table_name: str = "custom_data",
    mappings: FieldMapping = Depends(),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return import_dataset_from_database(
            db,
            db_url,
            src_table,
            name,
            table_name,
            owner_id=current_user.id,
            mappings=mappings.mappings,
            skip_columns=mappings.skip_columns
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/preview-file/", response_model=ColumnPreviewResponse)
def preview_uploaded_file_columns(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        with open(f"/tmp/{file.filename}", "wb") as f:
            f.write(file.file.read())
        columns = preview_file_columns(f"/tmp/{file.filename}")
        return {"columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preview-db/", response_model=ColumnPreviewResponse)
def preview_database_table_columns(
    db_url: str,
    table_name: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        columns = preview_db_columns(db_url, table_name)
        return {"columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/map-and-import-file/")
def map_and_import_file(
    file: UploadFile = File(...),
    mappings: ColumnMappingRequest = Depends(),
    name: str = "Uploaded Dataset",
    table_name: str = "custom_data",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        with open(f"/tmp/{file.filename}", "wb") as f:
            f.write(file.file.read())

        from app.crud.data_importer import import_dataset_from_file
        result = import_dataset_from_file(
            db=db,
            file_path=f"/tmp/{file.filename}",
            name=name,
            table_name=table_name,
            owner_id=current_user.id,
            mappings=mappings.mappings,
            skip_columns=mappings.skip_columns
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/map-and-import-db/")
def map_and_import_database(
    db_url: str,
    src_table: str,
    mappings: ColumnMappingRequest = Depends(),
    name: str = "Database Dataset",
    table_name: str = "custom_data",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        from app.crud.data_importer import import_dataset_from_database
        result = import_dataset_from_database(
            db=db,
            db_url=db_url,
            src_table=src_table,
            name=name,
            table_name=table_name,
            owner_id=current_user.id,
            mappings=mappings.mappings,
            skip_columns=mappings.skip_columns
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))