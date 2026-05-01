# StageFear Breaker - Deployment Guide

## Overview

**StageFear Breaker** is a fully public, authentication-free AI-powered public speaking practice platform. No login or signup required—users can start practicing immediately.

### Key Features
✅ No authentication required  
✅ Single default user mode  
✅ Instant access - just open the app  
✅ Fully functional audio recording & analysis  
✅ Session tracking & performance metrics  
✅ Mobile-friendly interface  
✅ Light/Dark theme support  

---

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Database**: MySQL
- **Audio Processing**: SpeechRecognition, PyDub
- **Deployment**: Docker, Heroku, AWS, Azure, or any Python-capable hosting

---

## Prerequisites

- Python 3.9+
- MySQL 8.0+ (or compatible database)
- FFmpeg (for audio processing)
- pip (Python package manager)

---

## Local Setup

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd stagefear
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your database credentials
# Example:
# DATABASE_URL=mysql+pymysql://root:password@localhost:3306/stagefear
```

### 5. Ensure FFmpeg is Installed
**Windows:**
```bash
choco install ffmpeg
# or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### 6. Run the Application
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open browser: **http://localhost:8000**

---

## Database Setup

### Create MySQL Database
```sql
CREATE DATABASE stagefear;
-- The app will auto-create tables and a default user on first run
```

### Connection String Format
```
mysql+pymysql://username:password@host:port/database
```

### Example Configurations

**Local Development:**
```
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/stagefear
```

**Remote Server:**
```
DATABASE_URL=mysql+pymysql://user:secure_pass@db.example.com:3306/stagefear
```

**AWS RDS:**
```
DATABASE_URL=mysql+pymysql://admin:password@your-db.region.rds.amazonaws.com:3306/stagefear
```

---

## Deployment Options

### Option 1: Docker (Recommended)

#### Create `Dockerfile`
```dockerfile
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create `docker-compose.yml`
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: stagefear
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+pymysql://root:root_password@db:3306/stagefear
    depends_on:
      - db
    volumes:
      - .:/app

volumes:
  db_data:
```

#### Run with Docker
```bash
docker-compose up --build
```

---

### Option 2: Heroku

#### 1. Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows/Linux
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. Create Heroku Account and App
```bash
heroku login
heroku create your-app-name
```

#### 3. Add ClearDB MySQL Add-on
```bash
heroku addons:create cleardb:ignite
```

#### 4. Configure Heroku
```bash
# Get database URL
heroku config:get CLEARDB_DATABASE_URL

# Set it as DATABASE_URL
heroku config:set DATABASE_URL="<paste-from-above>"

# Add Procfile (already exists)
```

#### 5. Deploy
```bash
git push heroku main
```

Access: `https://your-app-name.herokuapp.com`

---

### Option 3: AWS EC2

#### 1. Launch EC2 Instance
- Ubuntu 20.04 LTS
- t2.micro or larger
- Security group: Allow HTTP (80), HTTPS (443), SSH (22)

#### 2. Connect and Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-public-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.9 python3-pip python3.9-venv ffmpeg mysql-client git

# Clone project
git clone <repo> && cd stagefear

# Create venv and install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Setup MySQL RDS
- Create RDS instance from AWS console
- Get endpoint and credentials
- Update `.env` with RDS connection string

#### 4. Run with Supervisor
```bash
sudo apt install supervisor

# Create /etc/supervisor/conf.d/stagefear.conf
sudo nano /etc/supervisor/conf.d/stagefear.conf
```

Paste:
```ini
[program:stagefear]
directory=/home/ubuntu/stagefear
command=/home/ubuntu/stagefear/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/stagefear.log
environment=DATABASE_URL="your-database-url"
```

Then:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start stagefear
```

---

### Option 4: Azure App Service

#### 1. Create App Service
```bash
az group create --name stagefear-rg --location eastus
az appservice plan create --name stagefear-plan --resource-group stagefear-rg --sku B1 --is-linux
az webapp create --resource-group stagefear-rg --plan stagefear-plan --name stagefear-app --runtime "PYTHON:3.9"
```

#### 2. Configure Database
- Create Azure Database for MySQL
- Get connection string

#### 3. Deploy from GitHub
```bash
# Configure deployment from GitHub repo
# Set environment variables in Azure Portal:
# DATABASE_URL=your-connection-string
```

---

## Production Checklist

### Security
- [ ] Database credentials stored in environment variables (not hardcoded)
- [ ] HTTPS enabled (use Let's Encrypt or CDN)
- [ ] CORS configured for your domain only
- [ ] Database backups enabled
- [ ] Regular security updates

### Performance
- [ ] Use Gunicorn for production:
  ```bash
  gunicorn -w 4 -b 0.0.0.0:8000 backend.main:app
  ```
- [ ] Enable gzip compression in nginx/reverse proxy
- [ ] Configure CDN for static files
- [ ] Database connection pooling enabled
- [ ] Static files served via reverse proxy (nginx/Apache)

### Monitoring
- [ ] Enable application logging
- [ ] Setup error tracking (Sentry, Rollbar)
- [ ] Monitor database performance
- [ ] Setup uptime monitoring
- [ ] Configure database backups

### Scaling
- [ ] Horizontal scaling with load balancer
- [ ] Database replication for high availability
- [ ] Redis caching layer (optional)
- [ ] Static file CDN

---

## Troubleshooting

### Audio Processing Issues
```bash
# Ensure FFmpeg is installed and in PATH
ffmpeg -version

# Test SpeechRecognition
python -c "import speech_recognition as sr; print(sr.__version__)"
```

### Database Connection Error
```bash
# Test MySQL connection
mysql -h your-host -u your-user -p

# Verify DATABASE_URL format
# Should be: mysql+pymysql://user:password@host:port/database
```

### Port Already in Use
```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn backend.main:app --port 8001
```

### Session Data Not Saving
- Check database is running
- Verify DATABASE_URL in environment
- Check database user has write permissions
- Review application logs

---

## API Endpoints (All Public - No Auth Required)

### Topics
```
POST /api/topics/generate       # Generate topic by category/difficulty
GET  /api/topics/today          # Get topic of the day
GET  /api/topics/surprise       # Get random topic
```

### Sessions
```
POST /api/sessions/analyze      # Record and analyze speech
GET  /api/sessions              # Get all sessions
GET  /api/sessions/{id}         # Get specific session
GET  /api/stats                 # Get user statistics
```

### Frontend
```
GET  /                          # Landing page
GET  /home                      # Home page
GET  /session                   # Practice session
GET  /dashboard                 # Dashboard/history
```

---

## File Structure

```
stagefear/
├── backend/
│   ├── main.py              # FastAPI app & routes
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # DB connection
│   ├── analysis.py          # Speech analysis
│   ├── topics.py            # Topic generation
│   └── __init__.py
├── templates/
│   ├── index.html           # Landing page
│   ├── home.html            # Home page
│   ├── session.html         # Practice interface
│   └── dashboard.html       # Dashboard/stats
├── static/
│   ├── css/
│   │   ├── main.css
│   │   ├── home.css
│   │   └── style.css
│   └── js/
│       ├── auth.js          # Redirect to home
│       ├── home.js          # Home page logic
│       ├── session.js       # Session logic
│       ├── dashboard.js     # Dashboard logic
│       └── script.js        # Utilities
├── recordings/              # Temp audio storage
├── requirements.txt         # Python dependencies
├── Procfile                 # Heroku deployment
├── .env.example             # Environment template
├── Dockerfile              # Docker image
└── docker-compose.yml      # Docker compose
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | MySQL connection string |
| `ENV` | No | `production` or `development` |
| `HOST` | No | Server host (default: 0.0.0.0) |
| `PORT` | No | Server port (default: 8000) |

---

## Support & Maintenance

### Regular Tasks
- Monitor application logs
- Review database backups
- Update dependencies monthly
- Monitor disk space

### Maintenance Windows
- Schedule database backups: Daily at 2 AM UTC
- Update dependencies: Monthly
- Security updates: As needed (ASAP)

---

## License

[Your License Here]

---

## Contact

For issues or questions:
- GitHub Issues: [your-repo]
- Email: support@stagefear.local

---

**Last Updated**: May 2026  
**Version**: 1.0.0 - No Auth  
**Status**: Production Ready ✅
