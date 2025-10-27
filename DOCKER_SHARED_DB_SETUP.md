# Docker Shared Database Setup ✅

## 🎯 What's Been Configured

Your NoteApp now has a **shared database setup** where:
- ✅ Docker container and local Python share **the same SQLite database**
- ✅ Code changes sync automatically (no rebuild needed)
- ✅ Data persists across all environments
- ✅ Works on any machine after git clone

---

## 📝 Changes Made

### 1. **docker-compose.yml** ✅
- Changed from named volume to bind mount for `data/` directory
- Now uses: `- ./data:/app/data`
- This allows both Docker and local Python to access the same database file

### 2. **.dockerignore** ✅
- Updated to exclude database files from image
- Database files are bind-mounted in docker-compose instead

### 3. **No code changes** ✅
- Django `settings.py` already uses `data/db.sqlite3`
- No Python/HTML/CSS/JS modified
- Project code remains untouched

---

## 🚀 How to Use

### Start Docker

```bash
docker-compose up -d
```

Visit: **http://localhost:8000**

### Run Locally

```bash
source venv/bin/activate
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

### The Magic: Both Use Same Database!

1. Create a note in Docker → See it in local Python ✅
2. Edit a note locally → See changes in Docker ✅
3. Register user in Docker → Login works locally ✅

---

## 📊 File Structure

```
NoteApp/
├── data/                   # ← Shared database directory
│   └── db.sqlite3         # Used by BOTH Docker and local Python
├── venv/                  # Local Python environment
├── Dockerfile             # Container definition
├── docker-compose.yml     # ← Updated to use bind mount
├── .dockerignore          # ← Updated to handle data properly
└── ...
```

---

## 🔍 Key Configuration

### docker-compose.yml
```yaml
volumes:
  - .:/app              # Full project sync (code changes)
  - ./data:/app/data    # Shared database directory
```

### settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data' / 'db.sqlite3',  # ← Shared location
    }
}
```

---

## ✅ Verification

### Test Shared Database

```bash
# 1. Start Docker
docker-compose up -d

# 2. Create data via Docker shell
docker exec -it noteapp python manage.py shell
>>> from notes.models import Note
>>> Note.objects.count()
2
>>> exit()

# 3. Check same data via local Python
source venv/bin/activate
python manage.py shell
>>> from notes.models import Note
>>> Note.objects.count()
2  # ← Same count! Database is shared!
```

---

## ⚠️ Important Notes

### Port Conflicts

**Don't run both on port 8000 at the same time!**

**Solution:**
- Run Docker: `docker-compose up -d` → http://localhost:8000
- Run local: `python manage.py runserver 8001` → http://127.0.0.1:8001

### SQLite Locking

Only **one writer** at a time. If you see:
```
sqlite3.OperationalError: database is locked
```

**Fix:** Stop one server before using the other.

---

## 🎉 Summary

**What you got:**
- ✅ Shared database between Docker and local Python
- ✅ Automatic code synchronization (no rebuild needed)
- ✅ Data persistence across all environments
- ✅ Perfect for team development
- ✅ Works immediately after git clone
- ✅ No project code modified

**Setup complete! Ready to use!** 🚀

