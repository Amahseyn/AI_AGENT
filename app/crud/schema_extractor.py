# app/crud/schema_extractor.py
import pandas as pd
from sqlalchemy import create_engine, inspect
from fastapi import UploadFile, HTTPException
from tempfile import NamedTemporaryFile
import os

def get_columns_from_file(file_path):
    _, ext = os.path.splitext(file_path)

    if ext == '.csv':
        df = pd.read_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    elif ext == '.json':
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: '{ext}'")

    return df.columns.tolist()


# crud/schema_extractor.py

def process_uploaded_file(file: UploadFile):
    try:
        with NamedTemporaryFile(delete=False) as tmp:
            contents = file.file.read()
            tmp.write(contents)
            tmp.flush()
            file_path = tmp.name

        # Use original filename for extension check
        _, ext = os.path.splitext(file.filename)

        df = pd.read_csv(file_path) if ext == '.csv' else \
             pd.read_excel(file_path) if ext in ['.xls', '.xlsx'] else \
             pd.read_json(file_path)

        result = [
            {
                "source_type": {
                    '.csv': 'csv',
                    '.xls': 'excel',
                    '.xlsx': 'excel',
                    '.json': 'json'
                }[ext],
                "source_name": file.filename,
                "column_name": col,
                "column_order": idx
            }
            for idx, col in enumerate(df.columns.tolist())
        ]

        os.unlink(file_path)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

def scan_database(db_url: str):
    try:
        engine = create_engine(db_url)
        inspector = inspect(engine)

        tables = inspector.get_table_names()
        result = []

        for table in tables:
            columns = [col['name'] for col in inspector.get_columns(table)]
            for idx, col in enumerate(columns):
                result.append({
                    "source_type": "database",
                    "source_name": table,
                    "column_name": col,
                    "column_order": idx
                })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")