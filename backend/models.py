from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("Session", back_populates="user")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    topic = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    difficulty = Column(String(50), nullable=False)

    transcript = Column(Text, default="")
    feedback = Column(Text, default="[]")

    word_count = Column(Integer, default=0)
    wpm = Column(Float, default=0)
    filler_count = Column(Integer, default=0)

    confidence_score = Column(Float, default=0)
    clarity_score = Column(Float, default=0)
    structure_score = Column(Float, default=0)
    overall_score = Column(Float, default=0)

    duration = Column(Float, default=60)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")