# 🚀 Quick Start Guide

**Get StageFear Breaker running in 5 minutes**

---

## Option 1: Local Development (Recommended for Testing)

### 1. Prerequisites
- Python 3.9+
- MySQL 8.0+
- FFmpeg installed

### 2. Clone & Setup
```bash
# Navigate to project
cd stagefear

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database
```bash
# Create .env file
cp .env.example .env

# Edit .env with your MySQL credentials
# DATABASE_URL=mysql+pymysql://root:password@localhost:3306/stagefear
```

### 4. Ensure MySQL is Running
```bash
# Create database (if not exists)
mysql -h localhost -u root -p -e "CREATE DATABASE stagefear;"
```

### 5. Run the App
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open Browser
```
http://localhost:8000
```

**That's it! 🎉**

---

## Option 2: Docker (Recommended for Production)

### 1. Prerequisites
- Docker
- Docker Compose

### 2. Run
```bash
docker-compose up --build
```

### 3. Open Browser
```
http://localhost:8000
```

**Done! 🎉**

---

## Option 3: Heroku (Quick Cloud Deploy)

### 1. Prerequisites
- Heroku CLI
- Git

### 2. Deploy
```bash
heroku login
heroku create your-app-name
heroku addons:create cleardb:ignite
heroku config:set DATABASE_URL="$(heroku config:get CLEARDB_DATABASE_URL)"
git push heroku main
```

### 3. Open
```
https://your-app-name.herokuapp.com
```

---

## Verify Installation

### ✅ Backend Working
```bash
curl http://localhost:8000/api/topics/today
# Should return a JSON topic
```

### ✅ Frontend Working
```bash
# Open in browser:
# http://localhost:8000
# Should load homepage without errors
```

### ✅ Database Connected
```bash
mysql -h localhost -u root -p stagefear -e "SELECT * FROM users WHERE id = 1;"
# Should show dummy user
```

---

## First Session

1. Open http://localhost:8000
2. Click "Start Practicing"
3. Select category & difficulty
4. Click "Generate Topic"
5. Prepare for 60 seconds
6. Speak for 60 seconds
7. Get instant feedback!
8. View results on dashboard

---

## Environment Variables

```bash
# Required
DATABASE_URL=mysql+pymysql://user:pass@host:3306/stagefear

# Optional
ENV=production
HOST=0.0.0.0
PORT=8000
```

---

## Troubleshooting

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### FFmpeg not found
```bash
# Ubuntu
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### Cannot connect to database
```bash
# Verify DATABASE_URL format:
# mysql+pymysql://username:password@hostname:3306/database

# Test connection:
mysql -h hostname -u username -p database
```

### Port 8000 already in use
```bash
# Use different port:
uvicorn backend.main:app --port 8001
```

### Microphone not working
- Check browser permissions
- Ensure HTTPS in production
- Test at: https://test.webrtc.org/

---

## Next Steps

- 📖 Read full [README.md](README.md)
- 🚀 See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- 📝 Check [MIGRATION.md](MIGRATION.md) for what changed
- 🐛 Report issues on GitHub

---

## Common Commands

```bash
# Development
uvicorn backend.main:app --reload

# Production
gunicorn -w 4 -b 0.0.0.0:8000 backend.main:app

# Docker
docker-compose up --build
docker-compose down

# Database
mysql -h localhost -u root -p stagefear

# Logs
tail -f /var/log/stagefear.log  # Linux
Get-Content -Tail 20 logs.txt   # Windows PowerShell
```

---

**Status**: ✅ Ready to Use  
**Docs**: See README.md  
**Help**: Check DEPLOYMENT.md
