from app import db, Note

db.create_all()

for i in range(50):
    note = Note(title=f'Note {i}', content=f'Content {i}')
    db.session.add(note)
db.session.commit()

print('Seeded')