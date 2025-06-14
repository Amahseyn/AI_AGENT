from sqlalchemy import Table, MetaData
from database.session import engine

def get_dynamic_table(table_name: str):
    metadata = MetaData(bind=engine)
    metadata.reflect()
    return metadata.tables.get(table_name)