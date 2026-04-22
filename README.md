# Productivity Notes App

A Flask API that lets users create and manage their own notes. Each user has their own account and can only see their own notes. This app uses authentication so you have to log in before you can use it.

## What You Need

- Python 3.8 or higher
- pip (comes with Python)
- pipenv (optional but recommended)

## How to Set This Up

### Step 1: Get the code
```bash
cd /path/to/FullAuthFlaskBackend-ProductivityApp/Full-Auth-Flask-Backend--Productivity-App
```

### Step 2: Make a virtual environment (so you don't mess up your computer)
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install the packages
```bash
pipenv install
```

Or if you don't use pipenv:
```bash
pip install -r requirements.txt
```

## How to Run It

### Step 1: Turn on the virtual environment
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 2: Load the database with test data (optional but helpful)
```bash
python seed.py
```

This creates 2 test users you can use:
- **User 1:** username is `john_doe`, password is `password123`
- **User 2:** username is `jane_smith`, password is `password456`

### Step 3: Start the server
```bash
python app.py
```

It should say something like "Running on http://localhost:5000" in your terminal. That means it's working!

## The Database

- **Type:** SQLite (it's a small simple database that works great for learning)
- **Location:** `instance/notes.db` (it gets made automatically)
- **Library:** SQLAlchemy (makes it easier to work with the database)

## How to Use the API

You have to log in before you can use the note stuff. 

### First, Sign Up (make an account)
```bash
POST /signup

{
  "username": "myusername",
  "email": "myemail@example.com",
  "password": "mypassword"
}
```

You get back:
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

You get back:
```json
{"message": "Logged in successfully", "user_id": 3}
```

### Check if You're Logged In
If you want to see who is logged in:
```bash
GET /check_session
```

You get back:
```json
{"user_id": 3, "username": "myusername", "email": "myemail@example.com"}
```

If you're not logged in:
```json
{"error": "Not logged in"}
```

### Log Out
```bash
POST /logout
```

You get back:
```json
{"message": "Logged out successfully"}
```

---

## Notes Stuff (you have to be logged in!)

### Get All Your Notes
```bash
GET /notes?page=1&per_page=5
```

You can change the page number and how many notes per page.

You get back:
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

### Make a New Note
```bash
POST /notes

{
  "title": "My Cool Note",
  "content": "Here is what I want to remember"
}
```

You get back:
```json
{
  "id": 1,
  "title": "My Cool Note",
  "content": "Here is what I want to remember",
  "created_at": "2026-04-22T10:00:00"
}
```

### Change a Note
```bash
PATCH /notes/1

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

You get back the updated note.

### Delete a Note
```bash
DELETE /notes/1
```

You get back:
```json
{"message": "Note deleted"}
```

---

## Testing with curl

Here's how to test this from the command line if you have `curl` installed:

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

### Make a note:
```bash
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"This is a test"}'
```

### Update a note (replace 1 with the note ID):
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

If you want to use a tool instead of curl:
1. Download Postman or Insomnia
2. Create requests for each endpoint
3. Remember to set `Content-Type: application/json` in the headers
4. Log in first before trying the note endpoints

## Folder Structure

```
.
├── app.py              # The main code - routes and models
├── seed.py             # Creates test users and notes
├── Pipfile             # Lists what packages we need
├── README.md           # This file
└── instance/
    └── notes.db        # The database (created when you run it)
```

## What Libraries We Used

- **Flask** - the web framework that makes the server
- **Flask-SQLAlchemy** - connects Flask to the database
- **Flask-Bcrypt** - hashes passwords so they're not stored plain text
- **Flask-Migrate** - for managing database updates
- **Flask-RESTful** - helps make REST APIs
- **Marshmallow** - for working with data
- **Pytest** - for testing (if we add tests)

## What This App Does

✅ Users can make accounts and log in
✅ Passwords are hashed using bcrypt
✅ Users can only see their own notes
✅ Notes have a title, content, and creation date
✅ You can create, read, update, and delete notes
✅ Notes are split into pages (pagination)
✅ The API returns the right error codes

## Troubleshooting

### Port 5000 is already being used
Edit the last line of app.py and change it to use a different port:
```python
app.run(debug=True, port=5001)
```

### Database got messed up
Delete `instance/notes.db` and run:
```bash
python seed.py
```

### Getting "Not logged in" error
Make sure you logged in first! Call `/login` or `/signup` before trying to use notes.

### What's my Python version?
Run this:
```bash
python --version
```

It should be 3.8 or higher.

## Things I Learned Making This

- How Flask works and making routes
- Using SQLAlchemy to work with databases
- Password hashing with bcrypt
- User authentication and sessions
- User isolation (users can only see their own data)
- Pagination (splitting results into pages)
- HTTP status codes and when to use them
- Making a REST API

## License

MIT License (you can use this for whatever)
