# Docker Setup Guide - Shared Database Development

## 🎯 Goal

This setup allows you to:
- ✅ Run NoteApp in Docker **AND** locally with VS Code/`runserver`
- ✅ Both environments share the **same SQLite database** in `data/db.sqlite3`
- ✅ Code changes sync **automatically** (no rebuild needed)
- ✅ Data persists across container restarts
- ✅ Works on any machine that clones the repo

---

## 📁 How It Works

### Shared Database
```
Project Root/
├── data/
│   └── db.sqlite3          # ← Shared by both Docker and local Python
├── Dockerfile
├── docker-compose.yml
└── ...
```

**Key Configuration:**
1. **settings.py** uses `data/db.sqlite3` (already configured)
2. **docker-compose.yml** bind-mounts `./data:/app/data`
3. **Local Python** and **Docker** both access `./data/db.sqlite3`

### Code Synchronization
```yaml
volumes:
  - .:/app              # Full project mount (real-time code sync)
  - ./data:/app/data    # Shared database directory
```

Any code change → instantly visible in Docker (no rebuild!)

---

## 🚀 Usage

### Start Docker Container

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

Visit: **http://localhost:8000**

### Run Locally (VS Code / Terminal)

```bash
# Activate virtual environment
source venv/bin/activate

# Run server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

### Switch Between Environments

**Both use the same data!**

1. Create a note in Docker → See it in local Python ✅
2. Edit a note locally → See changes in Docker ✅
3. Register user in Docker → Login works locally ✅

---

## 🔧 Development Workflow

### Edit Code in VS Code

1. Make changes to any Python/HTML/CSS/JS files
2. **No rebuild needed!** Changes are live in Docker
3. Just refresh the browser

### Create/Edit Notes

1. **In Docker:** http://localhost:8000
2. **Or locally:** http://127.0.0.1:8000
3. **Same database!** Changes appear in both

### Run Migrations

**Option 1: In Docker**
```bash
docker exec -it noteapp python manage.py migrate
```

**Option 2: Locally**
```bash
source venv/bin/activate
python manage.py migrate
```

**Both update the same database file!**

---

## 📝 File Structure

```
NoteApp/
├── data/                    # Shared database directory
│   └── db.sqlite3          # ← Shared by both environments
├── venv/                    # Local Python environment
├── static/                  # CSS, JS files
├── templates/              # HTML templates
├── notes/                   # Django app
├── note_project/           # Django project settings
├── Dockerfile              # Container definition
├── docker-compose.yml      # Container orchestration
├── start.sh                # Startup script
├── .dockerignore           # Files to exclude from Docker
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── README.md              # Documentation
```

---

## 🛠️ Key Features

### 1. Shared Database
```yaml
# docker-compose.yml
volumes:
  - .:/app              # Full project sync
  - ./data:/app/data    # Shared SQLite database
```

### 2. Auto Migrations
```bash
# start.sh runs migrations automatically
python manage.py migrate
```

### 3. Live Code Sync
- Edit files in VS Code → Changes in container
- No rebuild needed
- Just refresh browser

### 4. Data Persistence
- Docker uses `./data/db.sqlite3`
- Local Python uses `./data/db.sqlite3`
- Same file = same data

---

## 🐳 Docker Commands

```bash
# Start container
docker-compose up -d

# Stop container
docker-compose down

# View logs
docker-compose logs -f

# Access container shell
docker exec -it noteapp bash

# Run Django commands
docker exec -it noteapp python manage.py migrate
docker exec -it noteapp python manage.py createsuperuser
docker exec -it noteapp python manage.py shell

# Rebuild image (only if dependencies change)
docker-compose up -d --build
```

---

## 💻 Local Python Commands

```bash
# Activate environment
source venv/bin/activate

# Run server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run Django shell
python manage.py shell
```

---

## ⚠️ Important Notes

### Port Conflicts

**Don't run both at the same time on port 8000!**

**Solution:**
- Run **Docker** on port 8000: `docker-compose up -d`
- Run **local** on port 8001: `python manage.py runserver 8001`

OR

- Stop one before starting the other

### Database Locking

SQLite can only have **one writer at a time**. If you see:
```
sqlite3.OperationalError: database is locked
```

**Solution:** Stop one server before using the other

### Shared Data Directory

The `data/` directory is **not** in `.dockerignore` because:
- It's bind-mounted for sharing
- Both environments need access
- It's git-ignored (in `.gitignore`)

---

## ✅ Verification

### Check Shared Database

```bash
# Create data in Docker
docker exec -it noteapp python manage.py shell
>>> from notes.models import Note
>>> Note.objects.count()
```

```bash
# Check same data locally
source venv/bin/activate
python manage.py shell
>>> from notes.models import Note
>>> Note.objects.count()
# Should show the same count!
```

### Check Code Sync

1. Edit a Python file in VS Code
2. Check in Docker logs: `docker-compose logs -f`
3. Should see: "Watching for file changes"

---

## 🎉 Summary

**Your setup now:**
- ✅ Docker and local Python share the same database
- ✅ Code changes sync automatically (no rebuild)
- ✅ Data persists across all environments
- ✅ Perfect for team development
- ✅ Works immediately after git clone

**Ready to use!** 🚀

