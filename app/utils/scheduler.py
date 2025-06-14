from sqlalchemy import create_engine, inspect

def get_tables_from_db(db_url: str):
    engine = create_engine(db_url)
    inspector = inspect(engine)
    return inspector.get_table_names()

def load_table_to_dataframe(db_url: str, table_name: str):
    engine = create_engine(db_url)
    return pd.read_sql_table(table_name, con=engine)