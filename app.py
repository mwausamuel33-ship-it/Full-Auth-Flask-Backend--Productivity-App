import os
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

# Configure the app - using SQLite because it's simple and doesn't need a separate server
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///notes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super_secret_key_change_this')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


# User model - stores account info
# passwords are hashed so they're never stored as plain text
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # one user can have many notes
    notes = db.relationship('Note', backref='user', lazy=True, cascade='all, delete-orphan')


# Note model - each note belongs to a user
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# helper function to get the logged in user's id from the session
def get_current_user_id():
    return session.get('user_id')


# ---- Auth Routes ----

# Sign up - creates a new user account
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # make sure all required fields are included
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400

    # check if someone already has that username
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already taken'}), 400

    # check if email is already registered
    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_email:
        return jsonify({'error': 'Email already registered'}), 400

    # hash the password before saving - never store plain text passwords!
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    # log the user in right after signing up
    session['user_id'] = new_user.id

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201


# Login - checks credentials and starts a session
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400

    # look up the user by username
    user = User.query.filter_by(username=data['username']).first()

    # if user doesn't exist or password is wrong, return the same error message
    # (don't tell them which one is wrong - that's a security thing I learned)
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    # save user id in session so they stay logged in
    session['user_id'] = user.id

    return jsonify({'message': 'Logged in successfully', 'user_id': user.id}), 200


# Logout - clears the session
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


# Check session - used by the frontend to see if the user is still logged in
@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = get_current_user_id()

    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    }), 200


# ---- Notes Routes ----
# All of these require the user to be logged in

# Get all notes for the logged in user - supports pagination
@app.route('/notes', methods=['GET'])
def get_notes():
    user_id = get_current_user_id()

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # get page and per_page from query params, default to page 1 with 5 notes
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # only get notes that belong to the logged in user
    paginated_notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    notes_list = [
        {'id': note.id, 'title': note.title, 'content': note.content, 'created_at': note.created_at.isoformat()}
        for note in paginated_notes.items
    ]

    return jsonify({
        'notes': notes_list,
        'total': paginated_notes.total,
        'pages': paginated_notes.pages,
        'current_page': paginated_notes.page
    }), 200


# Create a new note
@app.route('/notes', methods=['POST'])
def create_note():
    user_id = get_current_user_id()

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()

    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400

    new_note = Note(
        title=data['title'],
        content=data['content'],
        user_id=user_id
    )
    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        'id': new_note.id,
        'title': new_note.title,
        'content': new_note.content,
        'created_at': new_note.created_at.isoformat()
    }), 201


# Update a note by id
@app.route('/notes/<int:id>', methods=['PATCH'])
def update_note(id):
    user_id = get_current_user_id()

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    note = db.session.get(Note, id)

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    # make sure the note belongs to the logged in user
    if note.user_id != user_id:
        return jsonify({'error': 'Forbidden - this note belongs to another user'}), 403

    data = request.get_json()

    # only update fields that were actually sent
    if data.get('title'):
        note.title = data['title']
    if data.get('content'):
        note.content = data['content']

    db.session.commit()

    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat()
    }), 200


# Delete a note by id
@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    user_id = get_current_user_id()

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    note = db.session.get(Note, id)

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    # users should only be able to delete their own notes
    if note.user_id != user_id:
        return jsonify({'error': 'Forbidden - this note belongs to another user'}), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully'}), 200


if __name__ == '__main__':
    # debug mode is on by default for development, set FLASK_DEBUG=0 to turn it off
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(debug=debug_mode)
