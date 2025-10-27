# Django NoteApp

A simple, modern note-taking application built with Django and Bootstrap 5.

## Features

- User registration, login, and logout
- Create, edit, delete, and view notes
- User-specific notes (users can only see their own notes)
- Modern Bootstrap 5 UI
- Responsive design
- CSRF protection
- Django messages framework for notifications

## Setup Instructions

### Option 1: Docker Setup (Recommended)

The easiest way to run the NoteApp is using Docker. This method handles all dependencies and setup automatically.

#### Quick Start (One Command)

```bash
./run_docker.sh run
```

Or using Docker Compose directly:

```bash
docker-compose up -d
```

The application will be available at `http://localhost:8000/`

#### Available Commands

- **Build the image**: `./run_docker.sh build`
- **Build and run**: `./run_docker.sh run`
- **Stop the container**: `./run_docker.sh stop`
- **View logs**: `docker-compose logs -f`
- **Access container shell**: `docker exec -it noteapp bash`

#### Pushing to Docker Hub

1. Edit `run_docker.sh` and replace `your-dockerhub-username` with your actual Docker Hub username
2. Run: `./run_docker.sh push`
3. The script will build, tag, and push the image to Docker Hub

#### Manual Docker Commands

```bash
# Build the image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down

# Tag and push to Docker Hub
docker build -t your-username/noteapp:latest .
docker push your-username/noteapp:latest
```

### Option 2: Local Python Setup

If you prefer to run the app locally without Docker:

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

#### 4. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
NoteApp/
├── note_project/          # Main project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── notes/                 # Notes app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── note_list.html
│   ├── note_form.html
│   └── note_confirm_delete.html
├── static/                # Static files (CSS, JS)
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Files to exclude from Docker build
├── run_docker.sh          # Helper script for Docker operations
├── data/                  # Database directory (created automatically)
├── manage.py
├── requirements.txt
└── README.md
```

## Usage

1. **Register**: Create a new account at `/register/`
2. **Login**: Access your account at `/login/`
3. **Create Notes**: Click "New Note" to create a note
4. **Edit Notes**: Click "Edit" on any note to modify it
5. **Delete Notes**: Click "Delete" on any note to remove it
6. **View Notes**: All your notes are displayed on the main page

## Models

- **Note**: Contains title, content, created_at, updated_at, and author (ForeignKey to User)

## Views

- **Authentication**: Custom login, register, and logout views
- **Note CRUD**: ListView, CreateView, UpdateView, DeleteView for notes
- **Security**: LoginRequiredMixin for protected views

## Templates

- **base.html**: Base template with Bootstrap navbar
- **login.html**: User login form
- **register.html**: User registration form
- **note_list.html**: Display all user notes
- **note_form.html**: Create/edit note form
- **note_confirm_delete.html**: Delete confirmation page
