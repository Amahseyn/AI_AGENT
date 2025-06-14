# app/crud/data_manager.py

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, inspect
from app.database.session import engine  # Make sure this path is correct
import pandas as pd


def create_table_from_df(df: pd.DataFrame, table_name: str):
    """
    Creates a new table dynamically based on DataFrame schema.
    If table exists, it will be dropped and recreated.
    """
    metadata = MetaData(bind=engine)

    # Drop existing table if exists
    if inspect(engine).has_table(table_name):
        Table(table_name, metadata, autoload_with=engine)
        metadata.drop_all(bind=engine)

    columns = []
    for col_name, dtype in df.dtypes.items():
        if dtype == 'int64':
            col_type = Integer
        elif dtype == 'float64':
            col_type = Float
        elif dtype == 'object':
            col_type = String
        else:
            col_type = String
        columns.append(Column(col_name, col_type))

    table = Table(table_name, metadata, *columns)
    metadata.create_all(engine)

    # Insert data
    with engine.connect() as conn:
        df.to_sql(table_name, con=conn, if_exists='append', index=False)


def apply_column_mapping(df: pd.DataFrame, mappings: dict, skip_columns: list) -> pd.DataFrame:
    """
    Rename and drop columns based on user-defined mapping.
    """
    # Rename columns
    df.rename(columns=mappings, inplace=True)

    # Drop skipped columns
    for col in skip_columns:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    return df


def get_all_records(table_name: str):
    """
    Fetch all records from a dynamically created table.
    """
    metadata = MetaData(bind=engine)
    try:
        table = Table(table_name, metadata, autoload_with=engine)
        with engine.connect() as conn:
            result = conn.execute(table.select())
            return [dict(row) for row in result]
    except Exception as e:
        raise ValueError(f"Error fetching records from {table_name}: {e}")


def update_record(table_name: str, record_id: int, updates: dict):
    """
    Update a single record by ID. Assumes table has an 'id' column.
    """
    metadata = MetaData(bind=engine)
    try:
        table = Table(table_name, metadata, autoload_with=engine)
        with engine.connect() as conn:
            stmt = table.update().where(table.c.id == record_id).values(**updates)
            conn.execute(stmt)
            conn.commit()
    except Exception as e:
        raise ValueError(f"Error updating record in {table_name}: {e}")


def delete_record(table_name: str, record_id: int):
    """
    Delete a record by ID.
    """
    metadata = MetaData(bind=engine)
    try:
        table = Table(table_name, metadata, autoload_with=engine)
        with engine.connect() as conn:
            stmt = table.delete().where(table.c.id == record_id)
            conn.execute(stmt)
            conn.commit()
    except Exception as e:
        raise ValueError(f"Error deleting record from {table_name}: {e}")


def upsert_into_table(df: pd.DataFrame, table_name: str):
    """
    Upsert DataFrame into a table.
    Currently replaces the table if exists; can be extended to support real upserts.
    """
    create_table_from_df(df, table_name)