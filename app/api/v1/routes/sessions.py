# app/api/v1/routes/sessions.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.session import SessionCreate, SessionResponse
from app.crud.session import create_session, get_sessions_by_user, get_session_by_id
from app.dependencies import get_current_user
from app.database.session import get_db

router = APIRouter(prefix="/session")


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_new_session(
    session: SessionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_session(db=db, session=session, owner_id=current_user.id)


@router.get("/", response_model=List[SessionResponse])
def list_sessions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_sessions_by_user(db=db, user_id=current_user.id)


@router.get("/{session_id}", response_model=SessionResponse)
def read_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_session = get_session_by_id(db=db, session_id=session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if db_session.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this session")
    return db_session