# app/models/schema_extractor.py
from sqlalchemy import Column, Integer, String
from database.session import Base

class SchemaMetadata(Base):
    __tablename__ = 'schema_metadata'

    id = Column(Integer, primary_key=True)
    source_type = Column(String)  # csv/excel/json/database
    source_name = Column(String)  # filename or table name
    column_name = Column(String)
    column_order = Column(Integer)