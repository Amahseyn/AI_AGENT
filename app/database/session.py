# app/database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,Session
from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True # Remove for async
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from typing import Generator

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI to inject a database session.
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()