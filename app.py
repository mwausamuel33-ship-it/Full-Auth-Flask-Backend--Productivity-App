# Import stuff
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Make the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Define the Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

# Route to get all notes
@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([{'id': n.id, 'title': n.title, 'content': n.content} for n in notes])

# Route to create a new note
@app.route('/notes', methods=['POST'])
def create_note():
    title = request.json['title']
    content = request.json['content']
    new_note = Note(title=title, content=content)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'id': new_note.id, 'title': new_note.title, 'content': new_note.content})

# Route to update a note
@app.route('/notes/<int:id>', methods=['PATCH'])
def update_note(id):
    note = Note.query.get(id)
    note.title = request.json.get('title', note.title)
    note.content = request.json.get('content', note.content)
    db.session.commit()
    return jsonify({'id': note.id, 'title': note.title, 'content': note.content})

# Route to delete a note
@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted'})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)