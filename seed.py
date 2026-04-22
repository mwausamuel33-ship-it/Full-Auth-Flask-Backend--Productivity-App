from app import app, db, User, Note
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Use app context
with app.app_context():
    db.create_all()

    # Create some users
    user1 = User(
        username='john_doe',
        email='john@example.com',
        password=bcrypt.generate_password_hash('password123').decode('utf-8')
    )

    user2 = User(
        username='jane_smith',
        email='jane@example.com',
        password=bcrypt.generate_password_hash('password456').decode('utf-8')
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create notes for user1
    for i in range(5):
        note = Note(
            title=f'John Note {i+1}',
            content=f'This is note {i+1} from John',
            user_id=user1.id
        )
        db.session.add(note)

    # Create notes for user2
    for i in range(5):
        note = Note(
            title=f'Jane Note {i+1}',
            content=f'This is note {i+1} from Jane',
            user_id=user2.id
        )
        db.session.add(note)

    db.session.commit()

    print('Seeded database with users and notes!')
