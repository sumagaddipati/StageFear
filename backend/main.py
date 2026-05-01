from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

import json
import random
import re
import io
import os
from pathlib import Path

from backend.database import SessionLocal, engine, Base
import backend.models as models
import backend.schemas as schemas
from backend.topics import get_topic, get_topic_of_day, TOPICS_DB
from backend.analysis import analyze_speech

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# ── DUMMY USER CONFIGURATION ────────────────────────────────────
# All sessions are associated with this default user ID
DUMMY_USER_ID = 1

Base.metadata.create_all(bind=engine)

# ── Initialize dummy user on startup ────────────────────────────
def init_dummy_user():
    """Ensure dummy user exists in database"""
    db = SessionLocal()
    try:
        existing_user = db.query(models.User).filter(models.User.id == DUMMY_USER_ID).first()
        if not existing_user:
            dummy_user = models.User(
                id=DUMMY_USER_ID,
                username="default_user",
                email="user@stagefear.local",
                hashed_password="not_applicable"
            )
            db.add(dummy_user)
            db.commit()
            print(f"✓ Dummy user (ID={DUMMY_USER_ID}) created successfully")
        else:
            print(f"✓ Dummy user (ID={DUMMY_USER_ID}) already exists")
    except Exception as e:
        print(f"⚠ Warning initializing dummy user: {e}")
        db.rollback()
    finally:
        db.close()

init_dummy_user()

init_dummy_user()

app = FastAPI(title="StageFear Breaker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = PROJECT_ROOT / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Serve frontend ──────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open(PROJECT_ROOT / "templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/home", response_class=HTMLResponse)
async def serve_home():
    with open(PROJECT_ROOT / "templates/home.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    with open(PROJECT_ROOT / "templates/dashboard.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/session", response_class=HTMLResponse)
async def serve_session():
    with open(PROJECT_ROOT / "templates/session.html", "r", encoding="utf-8") as f:
        return f.read()


# ── Topics ──────────────────────────────────────────────────────
@app.post("/api/topics/generate")
def generate_topic(req: schemas.TopicRequest, db: Session = Depends(get_db)):
    used_ids = req.used_topic_ids or []
    topic = get_topic(req.category, req.difficulty, used_ids)
    return topic


@app.get("/api/topics/today")
def topic_of_day():
    return get_topic_of_day()


@app.get("/api/topics/surprise")
def surprise_topic():
    cats = ["Tech", "Lifestyle", "Interview", "Fun", "Abstract"]
    diffs = ["Easy", "Medium", "Hard"]
    return get_topic(random.choice(cats), random.choice(diffs), [])


# ── Sessions ────────────────────────────────────────────────────
@app.post("/api/sessions/analyze")
async def analyze_session(
    audio: UploadFile = File(...),
    topic: str = Form(...),
    category: str = Form(...),
    difficulty: str = Form(...),
    duration: float = Form(...),
    db: Session = Depends(get_db)
):
    audio_bytes = await audio.read()
    result = analyze_speech(audio_bytes, duration, topic)

    session = models.Session(
        user_id=DUMMY_USER_ID,
        topic=topic,
        category=category,
        difficulty=difficulty,
        transcript=result["transcript"],
        word_count=result["word_count"],
        wpm=result["wpm"],
        filler_count=result["filler_count"],
        confidence_score=result["confidence_score"],
        clarity_score=result["clarity_score"],
        structure_score=result["structure_score"],
        overall_score=result["overall_score"],
        feedback=json.dumps(result["feedback"]),
        duration=duration,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    result["session_id"] = session.id
    return result


@app.get("/api/sessions")
def get_sessions(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    sessions = (
        db.query(models.Session)
        .filter(models.Session.user_id == DUMMY_USER_ID)
        .order_by(models.Session.created_at.desc())
        .limit(limit)
        .all()
    )
    return [schemas.SessionOut.from_orm(s) for s in sessions]


@app.get("/api/sessions/{session_id}")
def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    session = db.query(models.Session).filter(
        models.Session.id == session_id,
        models.Session.user_id == DUMMY_USER_ID
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return schemas.SessionOut.from_orm(session)


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    sessions = db.query(models.Session).filter(models.Session.user_id == DUMMY_USER_ID).all()
    if not sessions:
        return {"total": 0, "avg_score": 0, "avg_wpm": 0, "best_score": 0, "sessions_by_day": [], "score_trend": []}

    scores = [s.overall_score for s in sessions]
    wpms = [s.wpm for s in sessions]

    # Score trend (last 10)
    trend = [{"date": s.created_at.strftime("%b %d"), "score": s.overall_score, "wpm": s.wpm}
             for s in sorted(sessions, key=lambda x: x.created_at)[-10:]]

    # Category breakdown
    cat_map = {}
    for s in sessions:
        cat_map[s.category] = cat_map.get(s.category, [])
        cat_map[s.category].append(s.overall_score)
    cat_avg = {k: round(sum(v) / len(v)) for k, v in cat_map.items()}

    return {
        "total": len(sessions),
        "avg_score": round(sum(scores) / len(scores)),
        "avg_wpm": round(sum(wpms) / len(wpms)),
        "best_score": max(scores),
        "score_trend": trend,
        "category_avg": cat_avg,
        "weaknesses": _compute_weaknesses(sessions),
    }



def _compute_weaknesses(sessions):
    if not sessions:
        return []
    weaknesses = []
    avg_confidence = sum(s.confidence_score for s in sessions) / len(sessions)
    avg_clarity = sum(s.clarity_score for s in sessions) / len(sessions)
    avg_structure = sum(s.structure_score for s in sessions) / len(sessions)
    avg_wpm = sum(s.wpm for s in sessions) / len(sessions)

    if avg_confidence < 60:
        weaknesses.append({"label": "Confidence", "score": round(avg_confidence), "tip": "Practice power poses before speaking"})
    if avg_clarity < 60:
        weaknesses.append({"label": "Clarity", "score": round(avg_clarity), "tip": "Reduce filler words like 'um', 'uh', 'like'"})
    if avg_structure < 60:
        weaknesses.append({"label": "Structure", "score": round(avg_structure), "tip": "Use the rule: Intro → 3 Points → Conclusion"})
    if avg_wpm > 160:
        weaknesses.append({"label": "Pace", "score": 45, "tip": "Slow down — aim for 120–150 WPM"})
    elif avg_wpm < 80:
        weaknesses.append({"label": "Pace", "score": 45, "tip": "Speed up — you sound hesitant"})
    return weaknesses