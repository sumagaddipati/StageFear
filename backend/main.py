from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

import jwt
import bcrypt
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

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StageFear Breaker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "stagefear_secret_key_2024_xK9mP3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Mount static files
static_path = PROJECT_ROOT / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# ── Serve frontend ──────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open(PROJECT_ROOT / "templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    with open(PROJECT_ROOT / "templates/dashboard.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/session", response_class=HTMLResponse)
async def serve_session():
    with open(PROJECT_ROOT / "templates/session.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/home", response_class=HTMLResponse)
async def serve_home():
    with open(PROJECT_ROOT / "templates/home.html", "r", encoding="utf-8") as f:
        return f.read()


# ── Auth ────────────────────────────────────────────────────────
@app.post("/api/auth/signup", response_model=schemas.Token)
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = bcrypt.hashpw(user_in.password.encode(), bcrypt.gensalt()).decode()
    user = models.User(username=user_in.username, email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer", "username": user.username}


@app.post("/api/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not bcrypt.checkpw(form_data.password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer", "username": user.username}


@app.get("/api/auth/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user


# ── Topics ──────────────────────────────────────────────────────
@app.post("/api/topics/generate")
def generate_topic(req: schemas.TopicRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    used_ids = req.used_topic_ids or []
    topic = get_topic(req.category, req.difficulty, used_ids)
    return topic


@app.get("/api/topics/today")
def topic_of_day():
    return get_topic_of_day()


@app.get("/api/topics/surprise")
def surprise_topic(current_user: models.User = Depends(get_current_user)):
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
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    audio_bytes = await audio.read()
    result = analyze_speech(audio_bytes, duration, topic)

    session = models.Session(
        user_id=current_user.id,
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
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = (
        db.query(models.Session)
        .filter(models.Session.user_id == current_user.id)
        .order_by(models.Session.created_at.desc())
        .limit(limit)
        .all()
    )
    return [schemas.SessionOut.from_orm(s) for s in sessions]


@app.get("/api/sessions/{session_id}")
def get_session(
    session_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(models.Session).filter(
        models.Session.id == session_id,
        models.Session.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return schemas.SessionOut.from_orm(session)


@app.get("/api/stats")
def get_stats(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    sessions = db.query(models.Session).filter(models.Session.user_id == current_user.id).all()
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