from sqlalchemy.orm import Session
from app.models.imported_data import ImportedDataset
from app.schemas.imported_data import DatasetCreate
from app.utils.file_loader import load_file_to_dataframe
from app.utils.db_loader import load_table_to_dataframe
from app.crud.data_manager import create_table_from_df, apply_column_mapping
from app.utils.file_loader import get_file_columns
from app.utils.db_loader import get_db_table_columns


def preview_file_columns(file_path: str) -> list:
    return get_file_columns(file_path)


def preview_db_columns(db_url: str, table_name: str) -> list:
    return get_db_table_columns(db_url, table_name)

def import_dataset_from_file(
    db: Session,
    file_path: str,
    name: str,
    table_name: str,
    owner_id: int,
    mappings: dict = None,
    skip_columns: list = None
):
    df = load_file_to_dataframe(file_path)
    df = apply_column_mapping(df, mappings or {}, skip_columns or [])
    create_table_from_df(df, table_name)

    dataset = DatasetCreate(name=name, source_type="file", table_name=table_name)
    db_dataset = ImportedDataset(**dataset.model_dump(), owner_id=owner_id)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


def import_dataset_from_database(
    db: Session,
    db_url: str,
    src_table: str,
    name: str,
    table_name: str,
    owner_id: int,
    mappings: dict = None,
    skip_columns: list = None
):
    df = load_table_to_dataframe(db_url, src_table)
    df = apply_column_mapping(df, mappings or {}, skip_columns or [])
    create_table_from_df(df, table_name)

    dataset = DatasetCreate(name=name, source_type="database", table_name=table_name)
    db_dataset = ImportedDataset(**dataset.model_dump(), owner_id=owner_id)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset