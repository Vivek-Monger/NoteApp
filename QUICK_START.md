# Quick Start Guide - NoteApp

## 🚀 Choose Your Setup

You have **two ways** to run NoteApp. **Pick ONE** - don't run both at the same time!

---

## Option 1: Local Python (Recommended for Development) ⚡

**Best for:** Fast development, quick testing, making code changes

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run the server
python manage.py runserver

# 3. Open browser
# Visit: http://localhost:8000 or http://127.0.0.1:8000
# (They're the same thing!)
```

**To stop:** Press `Ctrl+C` in terminal

---

## Option 2: Docker (Recommended for Production) 🐳

**Best for:** Testing Docker setup, production-like environment, deployment

```bash
# 1. Make sure local server is stopped (Ctrl+C)
# 2. Start Docker
docker-compose up -d

# 3. Open browser
# Visit: http://localhost:8000

# 4. View logs
docker-compose logs -f

# 5. Stop Docker
docker-compose down
```

---

## ⚠️ Common Issue: Port 8000 Already in Use

### If you see: "Address already in use" or port conflicts

**Solution:** Stop whatever is using port 8000

```bash
# Check what's using port 8000
lsof -ti:8000

# Kill the process (use the PID from above)
kill -9 <PID>

# Or just stop Docker
docker-compose down
```

---

## 📊 Understanding localhost vs 127.0.0.1

| URL | What it means | Works? |
|-----|---------------|--------|
| `http://localhost:8000` | Your local computer | ✅ Yes |
| `http://127.0.0.1:8000` | Your local computer (IP) | ✅ Yes |
| `http://0.0.0.0:8000` | Not a valid URL | ❌ No |

**Important:** `localhost` and `127.0.0.1` are **the same thing!**

Docker shows `0.0.0.0` internally (to accept external connections), but you still access it via `localhost`.

---

## 🎯 My Recommendation

### For Daily Development:
```bash
source venv/bin/activate
python manage.py runserver
```
Then visit: http://localhost:8000

### For Testing Docker:
```bash
# Stop local server first (Ctrl+C)
docker-compose up -d
```
Then visit: http://localhost:8000

---

## ✅ Setup Check

```bash
# Check if virtual environment has Django
source venv/bin/activate
python -c "import django; print('✅ Django', django.__version__)"

# Check if Docker is running
docker-compose ps

# Check what's on port 8000
lsof -ti:8000
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
# Stop the server using it
docker-compose down
# Or kill the process
kill -9 $(lsof -ti:8000)
```

### "Database error: no such table"
```bash
source venv/bin/activate
python manage.py migrate
```

---

## 📝 Quick Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

# Docker commands
docker-compose up -d        # Start
docker-compose down         # Stop
docker-compose logs -f      # View logs
```

---

## 🎉 You're All Set!

Both `localhost` and `127.0.0.1` are the same - use either one! 🚀

