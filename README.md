# 🎤 StageFear Breaker - No Auth Edition

**AI-powered public speaking coach with instant access. No login. No signup. Just start.**

![Status](https://img.shields.io/badge/status-production%20ready-green)
![Auth](https://img.shields.io/badge/authentication-removed-red)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/fastapi-latest-009688)

---

## ✨ What Changed

This version has **zero authentication**. Everything has been stripped down for instant public access:

### ✅ Removed
- ❌ JWT authentication
- ❌ Login/Signup pages  
- ❌ User registration system
- ❌ Password hashing (bcrypt)
- ❌ OAuth2PasswordBearer dependencies
- ❌ Token validation
- ❌ Protected routes
- ❌ Authorization headers

### ✅ Simplified
- ✓ Single default user (`DUMMY_USER_ID = 1`)
- ✓ All endpoints are public
- ✓ Direct access to `/home` on startup
- ✓ Session data stored under default user
- ✓ Zero authentication checks in frontend
- ✓ No localStorage token management

### ✅ Maintained
- ✓ Full audio recording capability
- ✓ Speech analysis & scoring
- ✓ Performance tracking
- ✓ Session history
- ✓ Dark/Light theme
- ✓ Responsive design
- ✓ All statistics & feedback

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone and setup
git clone <repo> && cd stagefear
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env with your MySQL credentials

# 4. Ensure FFmpeg is installed
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg
# Windows: choco install ffmpeg

# 5. Run
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open: **http://localhost:8000**

---

## 📋 System Architecture

### Database
- **Single User**: ID = 1 (default, auto-created on startup)
- **Sessions Table**: Stores all recordings, analysis, and scores
- **Auto-init**: Dummy user created automatically on first run

### Backend (FastAPI)
```python
DUMMY_USER_ID = 1  # All sessions use this user ID

# All endpoints are PUBLIC - no auth dependencies
@app.get("/api/sessions")        # Get all sessions
@app.post("/api/sessions/analyze") # Record and analyze
@app.get("/api/stats")           # Get statistics
@app.get("/api/topics/generate")  # Get practice topics
```

### Frontend (Vanilla JS)
```javascript
// No authentication required
// All localStorage auth code removed
// No token management
// Direct navigation allowed

// Users can immediately:
// 1. Open /home
// 2. Go to /session
// 3. Record audio
// 4. Get analysis
// 5. View dashboard
```

---

## 📁 File Structure

```
stagefear/
│
├── 📄 backend/
│   ├── main.py           ← FastAPI app, all public endpoints
│   ├── models.py         ← Database models (User, Session)
│   ├── schemas.py        ← Data validation schemas
│   ├── database.py       ← SQLAlchemy config
│   ├── analysis.py       ← Speech analysis engine
│   └── topics.py         ← Practice topic database
│
├── 📄 templates/
│   ├── index.html        → Redirects to /home
│   ├── home.html         → Homepage with hero
│   ├── session.html      ← Main practice interface
│   └── dashboard.html    ← User statistics & history
│
├── 📄 static/
│   ├── css/
│   │   ├── main.css      ← Session & Dashboard styles
│   │   ├── home.css      ← Homepage styles
│   │   └── style.css     ← Common utilities
│   └── js/
│       ├── auth.js       ← Redirects to /home (no auth)
│       ├── home.js       ← Homepage functionality
│       ├── session.js    ← Recording & analysis logic
│       ├── dashboard.js  ← Stats & history display
│       └── script.js     ← Utility functions
│
├── 📄 recordings/        ← Temp audio files
│
├── 📄 requirements.txt   ← Dependencies (auth libs removed)
├── 📄 Procfile           ← Heroku deployment config
├── 📄 .env.example       ← Environment template
├── 📄 Dockerfile         ← Docker image config
├── 📄 docker-compose.yml ← Local dev with Docker
├── 📄 DEPLOYMENT.md      ← Full deployment guide
└── 📄 README.md          ← This file
```

---

## 🔧 What Was Modified

### Backend (`backend/main.py`)

**Before:**
```python
from fastapi.security import OAuth2PasswordBearer
from backend.auth import get_current_user

@app.get("/api/sessions")
def get_sessions(current_user: User = Depends(get_current_user)):
    sessions = db.query(Session).filter(Session.user_id == current_user.id)
```

**After:**
```python
DUMMY_USER_ID = 1

@app.get("/api/sessions")
def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(Session).filter(Session.user_id == DUMMY_USER_ID)
    return [schemas.SessionOut.from_orm(s) for s in sessions]
```

### Frontend (`static/js/dashboard.js`)

**Before:**
```javascript
const token = localStorage.getItem('sf_token');
if (!token) window.location.href = '/';
const headers = { 'Authorization': 'Bearer ' + token };

fetch('/api/stats', { headers })
```

**After:**
```javascript
// No authentication required - app is fully public
const headers = {};  // Empty headers

fetch('/api/stats')  // No headers needed
```

### Requirements (`requirements.txt`)

**Before:**
```
passlib[bcrypt]    ← Password hashing (removed)
PyJWT              ← JWT tokens (removed)
```

**After:**
```
# Removed unnecessary auth libraries
# Cleaner, smaller deployment
```

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(150) UNIQUE,
    hashed_password VARCHAR(255),
    created_at TIMESTAMP
);

-- Dummy user auto-created:
-- INSERT INTO users VALUES (1, 'default_user', 'user@stagefear.local', 'not_applicable', NOW());
```

### Sessions Table
```sql
CREATE TABLE sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT FOREIGN KEY (users.id),  -- Always = 1
    topic VARCHAR(255),
    category VARCHAR(100),
    difficulty VARCHAR(50),
    transcript TEXT,
    feedback JSON,
    word_count INT,
    wpm FLOAT,
    filler_count INT,
    confidence_score FLOAT,
    clarity_score FLOAT,
    structure_score FLOAT,
    overall_score FLOAT,
    duration FLOAT,
    created_at TIMESTAMP
);
```

---

## 📡 API Endpoints (All Public)

### Topics
```
POST /api/topics/generate
  Request: {
    "category": "Tech" | "Lifestyle" | "Interview" | "Fun" | "Abstract",
    "difficulty": "Easy" | "Medium" | "Hard",
    "used_topic_ids": [...]
  }
  Response: { "id": 1, "text": "...", "category": "Tech", ... }

GET /api/topics/today
  Response: { "id": 5, "text": "Topic for today...", ... }

GET /api/topics/surprise
  Response: { "id": 8, "text": "Random topic...", ... }
```

### Sessions
```
POST /api/sessions/analyze
  FormData: {
    "audio": <File>,
    "topic": "Speaking about AI",
    "category": "Tech",
    "difficulty": "Medium",
    "duration": 60
  }
  Response: {
    "session_id": 123,
    "transcript": "...",
    "word_count": 150,
    "wpm": 125,
    "overall_score": 78,
    ...
  }

GET /api/sessions?limit=10
  Response: [ { session objects }, ... ]

GET /api/sessions/{session_id}
  Response: { session object }

GET /api/stats
  Response: {
    "total": 15,
    "avg_score": 72,
    "best_score": 89,
    "score_trend": [...],
    "weaknesses": [...],
    ...
  }
```

### Pages
```
GET /              → Redirects to /home
GET /home          → Homepage
GET /session        → Practice interface
GET /dashboard     → Statistics & history
GET /static/*      → CSS, JS, images
```

---

## 🎯 User Flow

```
1. User Opens App
   ↓
2. Redirected to /home (landing page)
   ↓
3. Click "Start Practicing" OR "Practice" button
   ↓
4. Select topic category & difficulty
   ↓
5. Generate topic OR use daily topic OR "Surprise Me"
   ↓
6. 60-second prep timer
   ↓
7. 60-second recording timer with waveform visualization
   ↓
8. Recording analyzed by AI
   ↓
9. Results displayed with scores & feedback
   ↓
10. View dashboard with history & stats
    ↓
11. Session data saved to database forever
```

---

## 🛠️ Development

### Running Tests
```bash
# Run with reload (auto-restart on changes)
uvicorn backend.main:app --reload

# Run with specific port
uvicorn backend.main:app --port 8001

# Run with multiple workers (production)
gunicorn -w 4 -b 0.0.0.0:8000 backend.main:app
```

### Database Inspection
```bash
# Connect to MySQL
mysql -h localhost -u root -p stagefear

# View dummy user
SELECT * FROM users WHERE id = 1;

# View all sessions
SELECT * FROM sessions;

# View session count
SELECT COUNT(*) FROM sessions WHERE user_id = 1;
```

### Debug Logs
```python
# Add to main.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log initialization
logger.info(f"Dummy user initialized: ID={DUMMY_USER_ID}")
```

---

## 🚀 Deployment

### Docker (Recommended)
```bash
# Build image
docker build -t stagefear .

# Run with MySQL
docker-compose up --build

# Access at http://localhost:8000
```

### Heroku
```bash
heroku create your-app-name
heroku addons:create cleardb:ignite
heroku config:set DATABASE_URL="<cleardb-url>"
git push heroku main
```

### AWS/Azure/GCP
See `DEPLOYMENT.md` for detailed cloud deployment guides

---

## ⚙️ Configuration

### Environment Variables
```bash
# .env file
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/stagefear
ENV=production
```

### Customize (Optional)
```python
# In backend/main.py
DUMMY_USER_ID = 1  # Change if needed

# In CORS middleware
allow_origins=["*"]  # Restrict to your domain in production
```

---

## 📊 Features

### Recording & Analysis
- ✅ Real-time waveform visualization
- ✅ Silence detection with alerts
- ✅ Audio quality monitoring
- ✅ Automatic transcript generation
- ✅ Speech speed analysis (WPM)

### Scoring System
- ✅ Confidence Score (0-100)
- ✅ Clarity Score (0-100)
- ✅ Structure Score (0-100)
- ✅ Overall Score (0-100)
- ✅ Filler word detection

### Insights
- ✅ Weakness identification
- ✅ Category breakdown
- ✅ Score trends over time
- ✅ Performance comparisons
- ✅ Personalized tips

### UI/UX
- ✅ Dark/Light theme
- ✅ Responsive design (mobile-friendly)
- ✅ Smooth animations
- ✅ Real-time feedback
- ✅ Progress tracking

---

## ⚠️ Limitations & Notes

1. **Single User**: All data stored under one user ID. Perfect for personal use or single-tenant scenarios.

2. **No User Isolation**: Session data is shared across all browser sessions. This is by design for a fully public app.

3. **Audio Processing**: Requires FFmpeg to be installed and in system PATH.

4. **Database**: Must have MySQL 8.0+ or compatible database.

5. **Microphone Access**: Browser must allow microphone access (popup on first use).

---

## 🔒 Security Notes

**No Authentication = No User Privacy**
- All users access the same data
- Session history is shared
- Recordings are stored server-side indefinitely
- Not suitable for multi-user enterprise use
- Perfect for personal coaching or internal demos

**Recommended for Production:**
- Only expose on private/internal networks
- Use HTTPS (SSL/TLS)
- Restrict database access
- Enable database backups
- Monitor access logs

---

## 📝 To-Do / Enhancements

- [ ] Add session deletion functionality
- [ ] Export session data to PDF
- [ ] Progress graphs and charts
- [ ] Leaderboard (optional)
- [ ] Share results with mentor
- [ ] Mobile app version
- [ ] Video recording support
- [ ] Multi-language UI

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/awesome`)
3. Commit changes (`git commit -am 'Add awesome feature'`)
4. Push to branch (`git push origin feature/awesome`)
5. Create Pull Request

---

## 📜 License

MIT License - See LICENSE file for details

---

## 📞 Support

### Common Issues

**"ModuleNotFoundError: No module named 'speech_recognition'"**
```bash
pip install SpeechRecognition
```

**"FFmpeg not found"**
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg

# Windows
choco install ffmpeg
```

**"Cannot connect to database"**
```bash
# Verify DATABASE_URL format
# mysql+pymysql://user:password@host:port/database

# Test connection
mysql -h host -u user -p database
```

**"Microphone not detected"**
- Check browser permissions
- Ensure camera/microphone not in use
- Test with: https://test.webrtc.org/

---

## 🎉 Credits

**StageFear Breaker** - No Auth Edition  
Built with ❤️ for public speaking enthusiasts

---

## 📈 Version History

### v1.0.0 - No Auth (Current)
- ✅ Removed all authentication
- ✅ Simplified to single default user
- ✅ Cleaned frontend JS
- ✅ Removed JWT/bcrypt dependencies
- ✅ Production-ready deployment

### v0.9.0 - With Auth
- Original version with login/signup
- JWT token management
- User registration

---

**Status**: ✅ Production Ready  
**Last Updated**: May 2026  
**Auth**: ❌ None Required  
**Access**: 🌍 Fully Public
