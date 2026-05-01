from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime
import json


class TopicRequest(BaseModel):
    category: str
    difficulty: str
    used_topic_ids: Optional[List[str]] = []


class SessionOut(BaseModel):
    id: int
    topic: str
    category: str
    difficulty: str
    transcript: str
    word_count: int
    wpm: float
    filler_count: int
    confidence_score: float
    clarity_score: float
    structure_score: float
    overall_score: float
    feedback: Any
    duration: float
    created_at: datetime

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = {
            "id": obj.id,
            "topic": obj.topic,
            "category": obj.category,
            "difficulty": obj.difficulty,
            "transcript": obj.transcript,
            "word_count": obj.word_count,
            "wpm": obj.wpm,
            "filler_count": obj.filler_count,
            "confidence_score": obj.confidence_score,
            "clarity_score": obj.clarity_score,
            "structure_score": obj.structure_score,
            "overall_score": obj.overall_score,
            "feedback": json.loads(obj.feedback) if obj.feedback else [],
            "duration": obj.duration,
            "created_at": obj.created_at,
        }
        return cls(**data)