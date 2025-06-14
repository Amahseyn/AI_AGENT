from sqlalchemy import create_engine, inspect
import pandas as pd
def get_tables_from_db(db_url: str):
    engine = create_engine(db_url)
    inspector = inspect(engine)
    return inspector.get_table_names()

def load_table_to_dataframe(db_url: str, table_name: str):
    engine = create_engine(db_url)
    return pd.read_sql_table(table_name, con=engine)


def get_db_table_columns(db_url: str, table_name: str) -> list:
    engine = create_engine(db_url)
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        raise ValueError(f"Table '{table_name}' not found")
    return [col['name'] for col in inspector.get_columns(table_name)]