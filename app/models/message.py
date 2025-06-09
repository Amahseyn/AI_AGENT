# models/message.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(Integer, ForeignKey("sessions.id"))

    # Relationships
    session = relationship("Session", back_populates="messages")