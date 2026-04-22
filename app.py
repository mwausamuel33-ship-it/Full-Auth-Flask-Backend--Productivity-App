# Import stuff
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

# Make the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SECRET_KEY'] = 'super_secret_key_change_this'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # This makes it so notes are connected to users
    notes = db.relationship('Note', backref='user', lazy=True, cascade='all, delete-orphan')

# Define the Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # This connects the note to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Auth Routes

# Route to sign up - creates a new user account
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    
    # Check if username and email and password are provided
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if username already exists in the database
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Check if email already exists
    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_email:
        return jsonify({'error': 'Email already exists'}), 400
    
    # Hash the password using bcrypt so it's not stored in plain text
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Create new user object
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    # Set the session so user is logged in after signup
    session['user_id'] = new_user.id
    
    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

# Route to log in with username and password
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    
    # Check if username and password are provided
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    # If user doesn't exist, return error
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Check if password is correct by comparing with hashed password
    if not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Set session so user stays logged in
    session['user_id'] = user.id
    
    return jsonify({'message': 'Logged in successfully', 'user_id': user.id}), 200

# Route to log out - clears the session
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

# Route to check if user is logged in and get their info
@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    
    # If no user_id in session, user is not logged in
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Get user from database
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Return user info
    return jsonify({'user_id': user.id, 'username': user.username, 'email': user.email}), 200

# Note Routes

# Route to get all notes with pagination
@app.route('/notes', methods=['GET'])
def get_notes():
    user_id = session.get('user_id')
    
    # Check if user is logged in
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Get pagination parameters from URL (page number and items per page)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    
    # Get notes for the logged in user with pagination
    notes_paginated = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    
    # Format notes for response
    notes_data = [{
        'id': n.id, 
        'title': n.title, 
        'content': n.content,
        'created_at': n.created_at.isoformat()
    } for n in notes_paginated.items]
    
    return jsonify({
        'notes': notes_data,
        'total': notes_paginated.total,
        'pages': notes_paginated.pages,
        'current_page': page
    }), 200

# Route to create a new note
@app.route('/notes', methods=['POST'])
def create_note():
    user_id = session.get('user_id')
    
    # Check if user is logged in
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Check if title and content are provided
    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Missing title or content'}), 400
    
    # Create new note for the user
    new_note = Note(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(new_note)
    db.session.commit()
    
    return jsonify({
        'id': new_note.id, 
        'title': new_note.title, 
        'content': new_note.content,
        'created_at': new_note.created_at.isoformat()
    }), 201

# Route to update a note
@app.route('/notes/<int:id>', methods=['PATCH'])
def update_note(id):
    user_id = session.get('user_id')
    
    # Check if user is logged in
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Get the note from database
    note = Note.query.get(id)
    
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Check if the note belongs to the user (can't update someone else's note)
    if note.user_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403
    
    data = request.json
    
    # Update the note with new data, or keep old data if not provided
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    db.session.commit()
    
    return jsonify({
        'id': note.id, 
        'title': note.title, 
        'content': note.content,
        'created_at': note.created_at.isoformat()
    }), 200

# Route to delete a note
@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    user_id = session.get('user_id')
    
    # Check if user is logged in
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Get the note from database
    note = Note.query.get(id)
    
    if not note:
        return jsonify({'error': 'Note not found'}), 404
    
    # Check if the note belongs to the user (can't delete someone else's note)
    if note.user_id != user_id:
        return jsonify({'error': 'Forbidden'}), 403
    
    # Delete the note
    db.session.delete(note)
    db.session.commit()
    
    return jsonify({'message': 'Note deleted'}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
