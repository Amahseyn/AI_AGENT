# app/api/v1/routes/messages.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.message import MessageCreate, MessageResponse
from app.crud.message import create_message, get_messages_by_session
from app.utils.security import get_current_user
from app.database.session import get_db

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Ensure session exists and belongs to user
    db_session = db.query(db.models.Session).filter(db.models.Session.id == message.session_id).first()
    if not db_session or db_session.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this session")
    
    return create_message(db=db, message=message)


@router.get("/{session_id}", response_model=list[MessageResponse])
def read_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Verify ownership
    db_session = db.query(db.models.Session).filter(db.models.Session.id == session_id).first()
    if not db_session or db_session.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this session")

    return get_messages_by_session(db=db, session_id=session_id)