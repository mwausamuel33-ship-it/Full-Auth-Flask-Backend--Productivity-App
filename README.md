# Productivity Notes App

A Flask API for managing personal notes with user authentication. Each user can create, read, update, and delete their own notes securely.

## Prerequisites

- **Python 3.8** or higher
- **pip** (Python package manager)
- **pipenv** (optional, for dependency management)

## Installation

### 1. Clone the repository
```bash
cd /path/to/FullAuthFlaskBackend-ProductivityApp/Full-Auth-Flask-Backend--Productivity-App
```

### 2. Create a virtual environment (optional but recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pipenv install
```
Or with pip:
```bash
pip install -r requirements.txt
```

## Running the App

### 1. Activate the virtual environment (if created)
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Seed the database (optional - creates sample users and notes)
```bash
python seed.py
```
This creates 2 sample users with notes:
- **User 1:** username: `john_doe`, password: `password123`
- **User 2:** username: `jane_smith`, password: `password456`

### 3. Run the Flask server
```bash
python app.py
```

The app will start on **http://localhost:5000** with debug mode enabled.

## Database

- **Type**: SQLite
- **Location**: `instance/notes.db`
- **ORM**: SQLAlchemy with Flask-SQLAlchemy

The database is automatically created when the app runs for the first time.

## API Endpoints

### Authentication Endpoints

#### Sign Up
Create a new user account.
```bash
POST /signup
Content-Type: application/json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "mypassword"
}
```
**Response (201)**: 
```json
{"message": "User created successfully", "user_id": 3}
```

#### Login
Log in with username and password.
```bash
POST /login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123"
}
```
**Response (200)**: 
```json
{"message": "Logged in successfully", "user_id": 1}
```

#### Logout
Log out and clear the session.
```bash
POST /logout
```
**Response (200)**: 
```json
{"message": "Logged out successfully"}
```

#### Check Session / Get Current User
Get information about the currently logged in user.
```bash
GET /check_session
```
**Response (200)**: 
```json
{"user_id": 1, "username": "john_doe", "email": "john@example.com"}
```
**Response (401)** if not logged in:
```json
{"error": "Not logged in"}
```

### Note Endpoints

All note endpoints require authentication. You must be logged in to access them.

#### Get All Notes (with Pagination)
Retrieve all notes for the logged in user.
```bash
GET /notes?page=1&per_page=5
```
**Response (200)**: 
```json
{
  "notes": [
    {"id": 1, "title": "My Note", "content": "Note content", "created_at": "2026-04-22T10:00:00"},
    {"id": 2, "title": "Another Note", "content": "More content", "created_at": "2026-04-22T11:00:00"}
  ],
  "total": 10,
  "pages": 2,
  "current_page": 1
}
```

#### Create a New Note
Create a new note for the logged in user.
```bash
POST /notes
Content-Type: application/json

{
  "title": "My Note",
  "content": "This is the note content"
}
```
**Response (201)**: 
```json
{"id": 1, "title": "My Note", "content": "This is the note content", "created_at": "2026-04-22T10:00:00"}
```

#### Update a Note
Update an existing note (must be the owner).
```bash
PATCH /notes/1
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```
**Response (200)**: 
```json
{"id": 1, "title": "Updated Title", "content": "Updated content", "created_at": "2026-04-22T10:00:00"}
```

#### Delete a Note
Delete a note (must be the owner).
```bash
DELETE /notes/1
```
**Response (200)**: 
```json
{"message": "Note deleted"}
```

## Testing the API

### Using curl

#### Sign Up
```bash
curl -X POST http://localhost:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass"}'
```

#### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","password":"password123"}'
```

#### Get All Notes (after login)
```bash
curl -b "cookies.txt" http://localhost:5000/notes
```

#### Create a Note (after login)
```bash
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Note","content":"Test content"}'
```

#### Update a Note
```bash
curl -X PATCH http://localhost:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated","content":"New content"}'
```

#### Delete a Note
```bash
curl -X DELETE http://localhost:5000/notes/1
```

#### Check Session
```bash
curl http://localhost:5000/check_session
```

#### Logout
```bash
curl -X POST http://localhost:5000/logout
```

### Using a tool like Postman or Insomnia
Import the endpoints listed above and test with the JSON payloads shown. Make sure to enable "Send cookies" for session persistence.

## Project Structure

```
.
├── app.py              # Main Flask application with all routes and models
├── seed.py             # Database seeding script
├── Pipfile             # Pipenv dependencies
├── README.md           # This file
└── instance/
    └── notes.db        # SQLite database (created on first run)
```

## Dependencies

- **Flask** 2.2.2 - Web framework
- **Flask-SQLAlchemy** 3.0.3 - ORM integration
- **Flask-Bcrypt** 1.0.1 - Password hashing
- **Flask-Migrate** 4.0.0 - Database migrations
- **Flask-RESTful** 0.3.9 - RESTful API extensions
- **Marshmallow** 3.20.1 - Serialization
- **Pytest** 7.2.0 - Testing framework

## Features

✅ User authentication (signup, login, logout)
✅ Session management
✅ Password hashing with bcrypt
✅ User isolation (users can only see their own notes)
✅ Full CRUD operations on notes
✅ Pagination for retrieving notes
✅ Proper HTTP status codes and error messages
✅ Protected routes with authorization checks

## Troubleshooting

### Port already in use
If port 5000 is already in use, modify the last line in app.py:
```python
app.run(debug=True, port=5001)
```

### Database issues
To reset the database, delete `instance/notes.db` and run:
```bash
python seed.py
```

### "Not logged in" error
Make sure you're logged in before accessing note endpoints. First call `/login` or `/signup` to get a session.

### Python version mismatch
Ensure you're using Python 3.8+:
```bash
python --version
```

## License

MIT License
