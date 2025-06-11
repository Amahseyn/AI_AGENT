from sqlalchemy.orm import Session
from app.models.message import Message as DbMessage
from app.schemas.message import MessageCreate

def create_message(db: Session, message: MessageCreate):
    db_message = DbMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_session(db: Session, session_id: int):
    return db.query(DbMessage).filter(DbMessage.session_id == session_id).all()

