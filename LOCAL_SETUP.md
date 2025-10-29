# Local Development Setup (Without Docker)

This guide shows you how to run the NoteApp locally using Python and a virtual environment.

## ✅ Setup Complete

Your environment has been set up with:
- Virtual environment created (`venv/`)
- All dependencies installed from `requirements.txt`
- Django and all required packages installed

## 🚀 Running the Server Locally

### Option 1: Quick Start

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the Django development server
python manage.py runserver
```

### Option 2: Run in One Line

```bash
source venv/bin/activate && python manage.py runserver
```

Then visit: **http://127.0.0.1:8000**

---

## 📋 Common Commands

### Activate Virtual Environment

```bash
source venv/bin/activate
```

You'll see `(NoteApp)` in your terminal prompt when activated.

### Deactivate Virtual Environment

```bash
deactivate
```

### Run Migrations

```bash
source venv/bin/activate
python manage.py migrate
```

### Create Superuser

```bash
source venv/bin/activate
python manage.py createsuperuser
```

### Run Django Shell

```bash
source venv/bin/activate
python manage.py shell
```

---

## 🔧 Troubleshooting

### If you get "ModuleNotFoundError: No module named 'django'"

**Solution:** Make sure the virtual environment is activated:

```bash
source venv/bin/activate
```

Check that `(NoteApp)` appears in your terminal prompt.

### If you need to reinstall dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### If you want to start fresh

```bash
# Delete old virtual environment
rm -rf venv

# Create a new one
python3 -m venv venv

# Activate and install
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📦 Installed Packages

Your `requirements.txt` includes:
- Django 4.2+
- Django REST Framework
- JWT authentication
- CORS headers

---

## 🐳 Docker vs Local

You now have two ways to run your app:

### Using Docker (Recommended for Production)
```bash
docker-compose up -d
```
Visit: http://localhost:8000

### Using Local Python (Great for Development)
```bash
source venv/bin/activate
python manage.py runserver
```
Visit: http://127.0.0.1:8000

---

## 💡 Tips

1. **Always activate the virtual environment** before running Django commands
2. **Port 8000** is used by Django's development server
3. **Port conflicts**: If port 8000 is busy, use a different port:
   ```bash
   python manage.py runserver 8080
   ```
4. **Auto-reload**: The server automatically reloads when you change Python code
5. **Keep venv/ out of Git**: The `.gitignore` already excludes it

---

## ✨ Your Setup is Ready!

You can now develop your NoteApp locally. Happy coding! 🚀

