from sqlalchemy.orm import Session
from app.models.imported_data import ImportedDataset
from app.schemas.imported_data import DatasetCreate
from app.utils.file_loader import load_file_to_dataframe
from app.utils.db_loader import load_table_to_dataframe
from app.crud.data_importer import create_table_from_df


def import_dataset_from_file(db: Session, file_path: str, name: str, table_name: str, owner_id: int):
    df = load_file_to_dataframe(file_path)
    create_table_from_df(df, table_name)

    dataset = DatasetCreate(name=name, source_type="file", table_name=table_name)
    db_dataset = ImportedDataset(**dataset.model_dump(), owner_id=owner_id)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


def import_dataset_from_database(db: Session, db_url: str, src_table: str, name: str, table_name: str, owner_id: int):
    df = load_table_to_dataframe(db_url, src_table)
    create_table_from_df(df, table_name)

    dataset = DatasetCreate(name=name, source_type="database", table_name=table_name)
    db_dataset = ImportedDataset(**dataset.model_dump(), owner_id=owner_id)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset