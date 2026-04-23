# Productivity Notes App

A secure Flask REST API for managing personal notes. Users register, log in, and can only access their own notes. Built with session-based authentication, Flask-SQLAlchemy, Flask-Migrate, and Flask-Bcrypt.

---

## Installation

**Prerequisites:** Python 3.8+, pipenv

```bash
# 1. Clone the repo and enter the project directory
cd Full-Auth-Flask-Backend--Productivity-App

# 2. Install dependencies
pipenv install

# 3. Initialize and apply database migrations
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# 4. (Optional) Seed the database with sample data
python seed.py
```

Seed creates two test accounts:
- `john_doe` / `password123`
- `jane_smith` / `password456`

---

## Running the App

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`.

---

## API Endpoints

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register a new user. Body: `{ username, email, password }` |
| POST | `/login` | Log in. Body: `{ username, password }` |
| POST | `/logout` | Log out (clears session) |
| GET | `/check_session` | Returns current logged-in user info, or 401 if not logged in |

### Notes (authentication required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes?page=1&per_page=5` | Get paginated list of the logged-in user's notes |
| POST | `/notes` | Create a note. Body: `{ title, content }` |
| PATCH | `/notes/<id>` | Update a note by ID. Body: `{ title?, content? }` |
| DELETE | `/notes/<id>` | Delete a note by ID |

All note endpoints return `401` if not logged in and `403` if the note belongs to another user.

---

## Project Structure

```
.
├── app.py          # Models and all route handlers
├── seed.py         # Seeds the database with sample users and notes
├── Pipfile         # Project dependencies
├── migrations/     # Flask-Migrate migration files
├── README.md
└── instance/
    └── notes.db    # SQLite database (auto-created)
```

---

## Dependencies

- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Bcrypt 1.0.1
- Flask-Migrate 4.0.0
- Flask-RESTful 0.3.9
- Marshmallow 3.20.1
- Faker 15.3.2
- Pytest 7.2.0
- Werkzeug 2.2.2
