from sqlalchemy.orm import Session
from app.models.session import Session as DbSession
from app.schemas.session import SessionCreate

def create_session(db: Session, session: SessionCreate, owner_id: int):
    db_session = DbSession(**session.dict(), owner_id=owner_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_sessions_by_user(db: Session, user_id: int):
    return db.query(DbSession).filter(DbSession.owner_id == user_id).all()

def get_session_by_id(db: Session, session_id: int):
    return db.query(DbSession).filter(DbSession.id == session_id).first()