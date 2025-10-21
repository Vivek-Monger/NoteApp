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

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

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
