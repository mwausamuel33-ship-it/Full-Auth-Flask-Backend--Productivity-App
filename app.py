from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content')

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

@app.route('/notes', methods=['GET'])
def get_notes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    notes = Note.query.paginate(page=page, per_page=per_page)
    return jsonify({'notes': notes_schema.dump(notes.items), 'total': notes.total, 'pages': notes.pages})

@app.route('/notes', methods=['POST'])
def create_note():
    title = request.json['title']
    content = request.json['content']
    new_note = Note(title=title, content=content)
    db.session.add(new_note)
    db.session.commit()
    return note_schema.jsonify(new_note)

@app.route('/notes/<int:id>', methods=['PATCH'])
def update_note(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404
    note.title = request.json.get('title', note.title)
    note.content = request.json.get('content', note.content)
    db.session.commit()
    return note_schema.jsonify(note)

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted'})

if __name__ == '__main__':
    app.run(debug=True)