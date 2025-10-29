# Django NoteApp Project Overview

## Project Purpose and Tech Stack

**Purpose**: The Django NoteApp is a modern, secure note-taking web application that allows users to create, read, update, and delete personal notes. It provides both a traditional web interface and a REST API, supporting user authentication and authorization. The application is designed for simplicity, security, and ease of deployment using Docker.

**Tech Stack**:
- **Backend Framework**: Django 4.2+ with Django REST Framework (DRF)
- **Authentication**: JWT (JSON Web Tokens) via djangorestframework-simplejwt
- **Database**: SQLite (development/production-ready with Docker volumes)
- **Frontend**: Bootstrap 5 for responsive web UI, Django templates
- **API**: RESTful API with JWT authentication
- **Containerization**: Docker and Docker Compose
- **CI/CD**: GitHub Actions
- **Security**: CORS headers, CSRF protection, secure JWT configuration
- **Development Tools**: Python 3.10+, pip, pytest, flake8

## File-by-File Explanation

### Entry Points and Main Modules

#### `manage.py`
- **Purpose**: Django's command-line utility for administrative tasks
- **Runtime Logic**: Entry point for Django management commands (migrate, runserver, createsuperuser, etc.)
- **Usage**: `python manage.py <command>`

#### `start.sh`
- **Purpose**: Startup script for Docker container initialization
- **Runtime Logic**:
  1. Creates `data/` directory for database persistence
  2. Runs database migrations (`python manage.py migrate`)
  3. Collects static files (`python manage.py collectstatic`)
  4. Starts Django development server on `0.0.0.0:8000`

#### `note_project/`
- **Main Django project configuration**
- `settings.py`: Core Django settings (installed apps, database, JWT config, CORS, etc.)
- `urls.py`: Root URL configuration, includes notes app URLs
- `wsgi.py`/`asgi.py`: WSGI/ASGI application entry points for deployment

#### `notes/` (Main Application)
- **`models.py`**: Defines the `Note` model with fields (title, content, author, timestamps)
- **`views.py`**: Web interface views (NoteListView, NoteCreateView, etc.) and API auth views
- **`api_views.py`**: DRF-based API views for notes CRUD and authentication
- **`api_auth_views.py`**: Custom JWT authentication views (register, login, logout, refresh)
- **`serializers.py`**: DRF serializers for User registration/login and Note CRUD
- **`urls.py`**: URL routing for both web and API endpoints
- **`forms.py`**: Django forms for user registration and note creation/editing
- **`utils.py`**: JWT token utilities (generation, response formatting)
- **`admin.py`**: Django admin configuration for Note model
- **`apps.py`**: Django app configuration
- **`migrations/`**: Database migration files (0001_initial.py creates Note table)

#### Docker Configuration
- **`Dockerfile`**: Multi-stage Docker build using Python 3.10-slim
- **`docker-compose.yml`**: Defines noteapp service with volume mounts and port mapping
- **`.dockerignore`**: Excludes unnecessary files from Docker build context

#### CI/CD
- **`.github/workflows/ci.yml`**: GitHub Actions workflow with test, docker-build, security, and summary jobs

#### Static Assets and Templates
- **`static/css/style.css`**: Custom CSS styles
- **`templates/`**: HTML templates (base.html, login.html, note_list.html, etc.)

### Runtime Logic Flow

1. **Web Interface**: User accesses `/` → `NoteListView` (requires login) → displays user's notes
2. **API Flow**: Client sends JWT-authenticated request → `api_views.py` → serializer validation → database operation
3. **Authentication**: Login form/API → `authenticate()` → JWT tokens generated → stored in client
4. **Database**: SQLite file in `data/db.sqlite3`, auto-created on first migration

## JWT Authentication Flow

The application implements JWT authentication with multiple API endpoints:

### Login Flow
1. **Client Request**: POST `/api/login/` or `/api/v1/login/` with `{"username": "...", "password": "..."}`
2. **Authentication**: `authenticate()` validates credentials
3. **Token Generation**: `get_tokens_for_user()` creates access + refresh tokens
4. **Response**: `{"access": "...", "refresh": "...", "user": {...}}`

### Token Refresh Flow
1. **Client Request**: POST `/api/token/refresh/` with `{"refresh": "refresh_token"}`
2. **Validation**: `RefreshToken(refresh_token)` validates and creates new access token
3. **Response**: `{"access": "new_access_token", "refresh": "new_refresh_token"}`

### Token Verification
- **Middleware**: `rest_framework_simplejwt.authentication.JWTAuthentication`
- **Header**: `Authorization: Bearer <access_token>`
- **Validation**: Automatic on protected endpoints (`@permission_classes([IsAuthenticated])`)
- **Expiration**: Access tokens expire in 60 minutes, refresh tokens in 7 days

### Logout Flow
1. **Client Request**: POST `/api/logout/` with `{"refresh": "refresh_token"}`
2. **Blacklisting**: `token.blacklist()` invalidates refresh token
3. **Response**: `{"message": "Logout successful"}`

## Database Setup and Data Persistence

### SQLite Configuration
- **Location**: `data/db.sqlite3` (created automatically)
- **Settings**: Defined in `note_project/settings.py` DATABASES dict
- **Migration**: `python manage.py migrate` applies schema changes

### Docker Volumes
- **Bind Mount**: `./data:/app/data` in `docker-compose.yml`
- **Purpose**: Persists database across container restarts/rebuilds
- **Shared Access**: Allows local Python development to share same database as Docker

### Schema
- **Users**: Django's built-in User model (username, email, password)
- **Notes**: Custom Note model with ForeignKey to User
- **Relationships**: One-to-many (User → Notes)

## Docker and Docker Compose Workflow

### Image Build Process
1. **Base Image**: `FROM python:3.10-slim`
2. **Dependencies**: Install gcc, copy `requirements.txt`, `pip install`
3. **Directories**: Create `/app/staticfiles` and `/app/data`
4. **Code Copy**: Copy entire project to `/app`
5. **Permissions**: Make `start.sh` executable
6. **CMD**: Execute `/app/start.sh`

### Container Runtime
- **Service**: `noteapp` in `docker-compose.yml`
- **Ports**: `8000:8000` (host:container)
- **Volumes**:
  - `.:/app` - Live code sync for development
  - `./data:/app/data` - Database persistence
- **Environment**: `DJANGO_ALLOWED_HOSTS=*`
- **Restart**: `unless-stopped`

### Workflow Commands
- **Build**: `docker-compose build`
- **Run**: `docker-compose up -d`
- **Stop**: `docker-compose down`
- **Logs**: `docker-compose logs -f`
- **Shell**: `docker exec -it noteapp bash`

## CI/CD Pipeline Breakdown

### Job: test
- **Purpose**: Run Python tests and linting on multiple Python versions (3.10, 3.11)
- **Steps**:
  1. Checkout code
  2. Setup Python with pip caching
  3. Install system deps (sqlite3)
  4. Install Python deps + testing tools (flake8, pytest-django)
  5. Lint with flake8 (syntax errors, complexity, line length)
  6. Run pytest on `test.py`
  7. Django deployment checklist (`python manage.py check --deploy`)

### Job: docker-build
- **Purpose**: Build and test Docker image
- **Steps**:
  1. Checkout code
  2. Setup Docker Buildx
  3. Build image with caching (`noteapp:test`)
  4. Test container startup (run on port 8001, check HTTP response)
  5. Push to Docker Hub (only on main branch with secrets)

### Job: security
- **Purpose**: Security scanning and dependency checks
- **Steps**:
  1. Checkout code
  2. Setup Python
  3. Install security tools (safety, bandit)
  4. Check vulnerabilities in dependencies
  5. Static security analysis with Bandit

### Job: summary
- **Purpose**: Aggregate results from all jobs
- **Dependencies**: Needs test, docker-build, security
- **Logic**: Reports status of each job, fails if any failed

## GitHub-CI-Docker-Deployment Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   GitHub    │────│     CI      │────│   Docker    │────│ Deployment  │
│   Push/PR   │    │   Actions   │    │    Build    │    │   Container │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
   Code Changes       Test & Lint        Image Build        Running App
   (main/master)      (pytest, flake8)   (Dockerfile)       (localhost:8000)
                      Security Scan      Volume Mounts      Database Persist
                      Docker Test        Push to Hub        Auto-restart
```

## Cleanup Suggestions

The following files appear to be documentation/setup guides that may not be essential for the core web application functionality. They could potentially be moved to a separate `docs/` directory or archived:

- `CI_FIX_SUMMARY.md`
- `CI_SETUP.md`
- `DOCKER_FIX.md`
- `DOCKER_GUIDE.md`
- `DOCKER_HUB_SETUP.md`
- `DOCKER_SETUP_GUIDE.md`
- `DOCKER_SHARED_DB_SETUP.md`
- `LOCAL_SETUP.md`
- `ports_explained.md`
- `QUICK_START.md`
- `SETUP_SUMMARY.md`

These files contain setup instructions and troubleshooting guides that are useful during development but not required for the application's runtime.

## Unresolved Issues

No merge conflicts or syntax errors detected in the current codebase. All Python files pass basic syntax validation.
