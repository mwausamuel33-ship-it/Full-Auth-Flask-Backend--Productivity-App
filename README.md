# Productivity Notes App

A Flask API that lets users create and manage their own notes. Each user has their own account and can only see their own notes. This app uses authentication so you have to log in before you can use it.

## What You Need (Prerequisites)

- Python 3.8 or higher
- pip (comes with Python)
- pipenv (optional but recommended)

## Installation Instructions

Follow these steps to install and set up the project:

### Step 1: Clone or download the project
```bash
cd /path/to/FullAuthFlaskBackend-ProductivityApp/Full-Auth-Flask-Backend--Productivity-App
```

### Step 2: Create a virtual environment
Creating a virtual environment keeps this project separate from other Python projects on your computer.

```bash
python3 -m venv .venv
```

### Step 3: Activate the virtual environment
This makes sure you're using the right Python packages for this project.

**On Mac/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### Step 4: Install all the required packages
```bash
pipenv install
```

If you don't have pipenv, you can use pip instead:
```bash
pip install -r requirements.txt
```

This will install:
- Flask (the web framework)
- Flask-SQLAlchemy (for the database)
- Flask-Bcrypt (for password hashing)
- And other dependencies listed in Pipfile

### Step 5: Verify installation
To make sure everything installed correctly, run:
```bash
python -c "import flask; print(f'Flask {flask.__version__} is installed')"
```

## How to Run the Application

Once you've completed the installation steps above, here's how to run the app:

### Step 1: Make sure the virtual environment is activated
```bash
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

### Step 2: Load test data (optional but recommended)
This creates sample users and notes you can use to test:
```bash
python seed.py
```

This creates 2 test users:
- **Username:** `john_doe` | **Password:** `password123`
- **Username:** `jane_smith` | **Password:** `password456`

### Step 3: Start the Flask server
```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

The app is now running! Visit `http://localhost:5000` to test the API.

## The Database

- **Type:** SQLite (a lightweight database, perfect for learning)
- **Location:** `instance/notes.db`
- **ORM:** SQLAlchemy (makes working with databases easier)

The database is created automatically when you run the app.

## How to Use the API

You must log in before using the note endpoints.

### First, Sign Up (create an account)
```bash
POST /signup

{
  "username": "myusername",
  "email": "myemail@example.com",
  "password": "mypassword"
}
```

Response:
```json
{"message": "User created successfully", "user_id": 3}
```

### Then, Log In
```bash
POST /login

{
  "username": "myusername",
  "password": "mypassword"
}
```

Response:
```json
{"message": "Logged in successfully", "user_id": 3}
```

### Check if You're Logged In
```bash
GET /check_session
```

Response (if logged in):
```json
{"user_id": 3, "username": "myusername", "email": "myemail@example.com"}
```

Response (if not logged in):
```json
{"error": "Not logged in"}
```

### Log Out
```bash
POST /logout
```

Response:
```json
{"message": "Logged out successfully"}
```

---

## Notes Endpoints (must be logged in!)

### Get All Your Notes
```bash
GET /notes?page=1&per_page=5
```

You can change the page number and how many notes per page.

Response:
```json
{
  "notes": [
    {
      "id": 1,
      "title": "My Note",
      "content": "This is what I wrote",
      "created_at": "2026-04-22T10:00:00"
    }
  ],
  "total": 10,
  "pages": 2,
  "current_page": 1
}
```

### Create a New Note
```bash
POST /notes

{
  "title": "My Cool Note",
  "content": "Here is what I want to remember"
}
```

Response:
```json
{
  "id": 1,
  "title": "My Cool Note",
  "content": "Here is what I want to remember",
  "created_at": "2026-04-22T10:00:00"
}
```

### Update a Note
```bash
PATCH /notes/1

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

Response: The updated note

### Delete a Note
```bash
DELETE /notes/1
```

Response:
```json
{"message": "Note deleted"}
```

---

## Testing with curl

Here are curl commands you can use to test the API from your terminal:

### Sign up:
```bash
curl -X POST http://localhost:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass"}'
```

### Log in:
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","password":"password123"}'
```

### Get notes:
```bash
curl http://localhost:5000/notes
```

### Create a note:
```bash
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"This is a test"}'
```

### Update a note:
```bash
curl -X PATCH http://localhost:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated","content":"New content"}'
```

### Delete a note:
```bash
curl -X DELETE http://localhost:5000/notes/1
```

### Check session:
```bash
curl http://localhost:5000/check_session
```

### Log out:
```bash
curl -X POST http://localhost:5000/logout
```

## Using Postman or Insomnia

If you prefer a graphical tool instead of curl:
1. Download [Postman](https://www.postman.com/downloads/) or [Insomnia](https://insomnia.rest/)
2. Create requests for each endpoint
3. Set `Content-Type: application/json` in the headers
4. Log in first before trying the note endpoints

## Project Structure

```
.
├── app.py              # Main Flask code with routes and models
├── seed.py             # Creates test users and notes
├── Pipfile             # Lists the project dependencies
├── README.md           # This file
└── instance/
    └── notes.db        # SQLite database (created when you run the app)
```

## Dependencies

- **Flask 2.2.2** - Web framework for creating the API
- **Flask-SQLAlchemy 3.0.3** - Connects Flask to the database
- **Flask-Bcrypt 1.0.1** - Hashes passwords for security
- **Flask-Migrate 4.0.0** - Manages database changes
- **Flask-RESTful 0.3.9** - Helps build REST APIs
- **Marshmallow 3.20.1** - Serializes/deserializes data
- **Pytest 7.2.0** - Framework for writing tests

## Features

✅ User signup and login
✅ Password hashing with bcrypt
✅ User authentication with sessions
✅ Users can only see their own notes
✅ Full CRUD operations on notes (Create, Read, Update, Delete)
✅ Pagination for retrieving notes
✅ Proper HTTP status codes and error messages

## Troubleshooting

### Port 5000 is already in use
If you get an error that port 5000 is already being used, edit the last line of `app.py`:

```python
app.run(debug=True, port=5001)
```

Then run the app on port 5001 instead.

### Database is corrupted or outdated
Delete the database file and reseed:
```bash
rm instance/notes.db
python seed.py
```

### "Not logged in" error when accessing notes
You must log in first! Call `/login` or `/signup` before accessing note endpoints.

### Virtual environment not activating
Make sure you're in the project directory:
```bash
cd /path/to/FullAuthFlaskBackend-ProductivityApp/Full-Auth-Flask-Backend--Productivity-App
source .venv/bin/activate
```

### Check your Python version
Some features require Python 3.8+:
```bash
python --version
```

## What I Learned

- Building a REST API with Flask
- Using SQLAlchemy for database management
- Password hashing and security with bcrypt
- User authentication and sessions
- Database relationships and user isolation
- Pagination and result limiting
- HTTP status codes and RESTful design
- Building and deploying a full-stack application

## License

MIT License
