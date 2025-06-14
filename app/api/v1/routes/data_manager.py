from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.schemas.data_manager import RecordUpdate
from app.crud.data_manager import get_all_records, update_record, delete_record
from app.database.session import get_db
from app.dependencies import get_current_user


router = APIRouter(prefix="/data")


@router.get("/{table_name}/records")
def list_records(table_name: str):
    return {"data": get_all_records(table_name)}


@router.put("/{table_name}/records/{record_id}")
def edit_record(table_name: str, record_id: int, payload: RecordUpdate):
    update_record(table_name, record_id, payload.updates)
    return {"message": "Record updated"}


@router.delete("/{table_name}/records/{record_id}")
def remove_record(table_name: str, record_id: int):
    delete_record(table_name, record_id)
    return {"message": "Record deleted"}


@router.post("/schedule/sync-db/")
def schedule_db_import(
    db_url: str,
    src_table: str,
    dest_table: str,
    interval_minutes: int = 60
):
    from app.utils.scheduler import schedule_db_sync
    schedule_db_sync(db_url, src_table, dest_table, interval_minutes)
    return {"message": f"Sync scheduled every {interval_minutes} mins"}