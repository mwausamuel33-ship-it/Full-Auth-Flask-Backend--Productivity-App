# Productivity Notes App

A simple Flask API for managing personal notes. This is a lightweight backend application built with Flask and SQLAlchemy for handling CRUD operations on notes.

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

### 2. Seed the database (optional - creates sample data)
```bash
python seed.py
```
This creates 50 sample notes in the SQLite database.

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

### Get all notes
```bash
GET /notes
```
**Response**: Array of note objects
```json
[
  {"id": 1, "title": "Note 1", "content": "Content 1"},
  {"id": 2, "title": "Note 2", "content": "Content 2"}
]
```

### Create a new note
```bash
POST /notes
Content-Type: application/json

{
  "title": "My Note",
  "content": "This is the note content"
}
```
**Response**: Created note object with ID

### Update a note
```bash
PATCH /notes/<id>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```
**Response**: Updated note object

### Delete a note
```bash
DELETE /notes/<id>
```
**Response**: Success message

## Testing the API

### Using curl
```bash
# Get all notes
curl http://localhost:5000/notes

# Create a note
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Note","content":"Test content"}'

# Update a note (replace 1 with actual note ID)
curl -X PATCH http://localhost:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated","content":"New content"}'

# Delete a note (replace 1 with actual note ID)
curl -X DELETE http://localhost:5000/notes/1
```

### Using a tool like Postman or Insomnia
Import the endpoints listed above and test with the JSON payloads shown.

## Project Structure

```
.
├── app.py              # Main Flask application
├── seed.py             # Database seeding script
├── Pipfile             # Pipenv dependencies
├── README.md           # This file
└── instance/
    └── notes.db        # SQLite database (created on first run)
```

## Dependencies

- **Flask** 2.2.2 - Web framework
- **Flask-SQLAlchemy** 3.0.3 - ORM integration
- **Flask-Migrate** 4.0.0 - Database migrations
- **Flask-Bcrypt** 1.0.1 - Password hashing
- **Flask-RESTful** 0.3.9 - RESTful API extensions
- **Marshmallow** 3.20.1 - Serialization
- **Pytest** 7.2.0 - Testing framework

## Troubleshooting

### Port already in use
If port 5000 is already in use, you can specify a different port:
```bash
python app.py --port 5001
```
Or modify the `app.run()` call in app.py.

### Database issues
To reset the database, delete `instance/notes.db` and run:
```bash
python seed.py
```

### Python version mismatch
Ensure you're using Python 3.8+:
```bash
python --version
```

## License

MIT License
