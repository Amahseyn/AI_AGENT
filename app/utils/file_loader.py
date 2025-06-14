import pandas as pd
import os

def load_file_to_dataframe(file_path: str):
    _, ext = os.path.splitext(file_path)
    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)
    elif ext == ".json":
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    

def get_file_columns(file_path: str) -> list:
    _, ext = os.path.splitext(file_path)
    if ext == ".csv":
        df = pd.read_csv(file_path, nrows=0)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path, nrows=0)
    elif ext == ".json":
        df = pd.read_json(file_path, nrows=0)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return df.columns.tolist()