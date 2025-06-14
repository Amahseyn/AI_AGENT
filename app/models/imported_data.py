from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.session import Base

class ImportedDataset(Base):
    __tablename__ = "imported_datasets"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    source_type = Column(String)  # csv/excel/json/database
    table_name = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))