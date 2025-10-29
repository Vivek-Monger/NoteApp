# Docker Setup Guide for NoteApp

This guide explains how to use Docker to run the NoteApp locally and deploy it to Docker Hub.

## 📋 Prerequisites

- Docker installed on your system
- Docker Compose installed (comes with Docker Desktop)
- Docker Hub account (for pushing images)

## 🚀 Quick Start

### Running with One Command

```bash
./run_docker.sh run
```

Or with Docker Compose:

```bash
docker-compose up -d
```

Then visit: **http://localhost:8000**

---

## 📝 Detailed Instructions

### 1. Build the Docker Image

```bash
docker-compose build
```

Or use the helper script:

```bash
./run_docker.sh build
```

### 2. Run the Container

```bash
docker-compose up -d
```

The `-d` flag runs the container in detached mode (background).

**Check if it's running:**

```bash
docker ps
```

You should see the `noteapp` container running.

### 3. View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f
```

### 4. Stop the Container

```bash
docker-compose down
```

This stops and removes the container.

**Note:** Your database (`db.sqlite3`) is preserved in a Docker volume, so your data won't be lost.

### 5. Remove Everything (Including Data)

```bash
docker-compose down -v
```

This removes the container AND the database volume.

---

## 🐳 Docker Hub Deployment

### Step 1: Update run_docker.sh

Edit `run_docker.sh` and replace `your-dockerhub-username` with your actual Docker Hub username:

```bash
DOCKER_HUB_USERNAME="your-actual-username"
```

### Step 2: Login to Docker Hub

```bash
docker login
```

Enter your Docker Hub username and password.

### Step 3: Push the Image

```bash
./run_docker.sh push
```

Or manually:

```bash
# Build the image
docker build -t your-username/noteapp:latest .

# Push to Docker Hub
docker push your-username/noteapp:latest
```

### Step 4: Pull and Run on Another Machine

```bash
docker pull your-username/noteapp:latest
docker run -p 8000:8000 your-username/noteapp:latest
```

---

## 🛠️ Useful Commands

### Access Container Shell

```bash
docker exec -it noteapp bash
```

### Run Django Commands

```bash
# Create a superuser
docker exec -it noteapp python manage.py createsuperuser

# Run Django shell
docker exec -it noteapp python manage.py shell

# Run tests
docker exec -it noteapp python manage.py test
```

### Rebuild Image After Code Changes

```bash
docker-compose build --no-cache
docker-compose up -d
```

### View Container Status

```bash
docker ps -a
```

### Remove Stopped Containers

```bash
docker container prune
```

---

## 📁 File Structure

```
NoteApp/
├── Dockerfile              # Image build instructions
├── docker-compose.yml      # Container orchestration
├── .dockerignore           # Files to exclude from build
├── run_docker.sh           # Helper script
├── data/                   # Database directory
│   └── db.sqlite3          # Database (created automatically)
└── staticfiles/            # Collected static files
```

---

## 🔍 Troubleshooting

### Port Already in Use

If port 8000 is already in use, you can change it in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Use port 8001 on host
```

### Container Won't Start

1. Check logs: `docker-compose logs`
2. Rebuild: `docker-compose build --no-cache`
3. Check Docker is running: `docker ps`

### Database Issues

Reset the database:

```bash
docker-compose down -v
docker-compose up -d
```

### Static Files Not Loading

The app uses Django's built-in static file serving for development. For production, use:
- Nginx
- AWS S3
- WhiteNoise

---

## 🎯 Production Notes

For production deployment:

1. **Change DEBUG to False** in `settings.py`
2. **Set a proper SECRET_KEY** (use environment variables)
3. **Use a PostgreSQL database** instead of SQLite
4. **Add Nginx** as a reverse proxy
5. **Use WhiteNoise** for static files
6. **Set proper ALLOWED_HOSTS**
7. **Use Gunicorn** instead of `runserver`

Example production Dockerfile:

```dockerfile
# Install gunicorn
RUN pip install gunicorn

# Change CMD to use gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "note_project.wsgi"]
```

---

## ✅ Summary

**Basic workflow:**

1. Clone the repo
2. Run: `./run_docker.sh run`
3. Visit: http://localhost:8000
4. Create account and start taking notes!

**To stop:**

```bash
./run_docker.sh stop
```

That's it! Happy note-taking! 📝

