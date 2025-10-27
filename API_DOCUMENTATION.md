# JWT Authentication API Documentation

This document describes the JWT-based authentication API endpoints for the Django NoteApp.

## Base URL
```
http://127.0.0.1:8000
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Endpoints

### 1. User Registration

**POST** `/api/register/`

Register a new user account.

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
}
```

**Response (201 Created):**
```json
{
    "message": "User created successfully",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    }
}
```

### 2. User Login

**POST** `/api/login/`

Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    }
}
```

### 3. Token Refresh

**POST** `/api/token/refresh/`

Refresh the access token using the refresh token.

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 4. User Logout

**POST** `/api/logout/`

Logout user and blacklist the refresh token.

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
    "message": "Logout successful"
}
```

### 5. User Profile

**GET** `/api/v1/profile/`

Get current user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
}
```

### 6. Notes List/Create

**GET** `/api/v1/notes/`

Get all notes for the authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "title": "My First Note",
        "content": "This is the content of my first note.",
        "author": "johndoe",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
]
```

**POST** `/api/v1/notes/`

Create a new note.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "title": "New Note",
    "content": "This is the content of the new note."
}
```

**Response (201 Created):**
```json
{
    "id": 2,
    "title": "New Note",
    "content": "This is the content of the new note.",
    "author": "johndoe",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

### 7. Note Detail

**GET** `/api/v1/notes/{id}/`

Get a specific note by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "My First Note",
    "content": "This is the content of my first note.",
    "author": "johndoe",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

**PUT** `/api/v1/notes/{id}/`

Update a specific note.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "title": "Updated Note Title",
    "content": "Updated content of the note."
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Updated Note Title",
    "content": "Updated content of the note.",
    "author": "johndoe",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:15:00Z"
}
```

**DELETE** `/api/v1/notes/{id}/`

Delete a specific note.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204 No Content):**
```json
{
    "message": "Note deleted successfully"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid JSON data"
}
```

### 401 Unauthorized
```json
{
    "error": "Invalid credentials"
}
```

### 404 Not Found
```json
{
    "error": "Note not found"
}
```

## JavaScript Usage Example

```javascript
// Login
const loginResponse = await fetch('/api/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'johndoe',
        password: 'securepassword123'
    })
});

const loginData = await loginResponse.json();
const accessToken = loginData.access;
const refreshToken = loginData.refresh;

// Store tokens
localStorage.setItem('access_token', accessToken);
localStorage.setItem('refresh_token', refreshToken);

// Make authenticated request
const notesResponse = await fetch('/api/v1/notes/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
    }
});

const notes = await notesResponse.json();
```

## Token Management

- **Access Token**: Short-lived (60 minutes), used for API requests
- **Refresh Token**: Long-lived (7 days), used to get new access tokens
- **Token Rotation**: Refresh tokens are rotated on each refresh
- **Blacklisting**: Refresh tokens are blacklisted on logout

## Security Features

- CSRF protection
- JWT token blacklisting
- Token rotation
- CORS configuration
- User-specific data isolation
