from app import app, db, bcrypt, User, Note

# This script seeds the database with some test users and notes
# Run it with: python seed.py

with app.app_context():

    # delete existing data first so we can re-run this without errors
    print('Clearing old data...')
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    print('Creating users...')

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

    print('Creating notes...')

    # create 5 notes for john
    for i in range(1, 6):
        note = Note(
            title=f'John Note {i}',
            content=f'This is note number {i} written by John.',
            user_id=user1.id
        )
        db.session.add(note)

    # create 5 notes for jane
    for i in range(1, 6):
        note = Note(
            title=f'Jane Note {i}',
            content=f'This is note number {i} written by Jane.',
            user_id=user2.id
        )
        db.session.add(note)

    db.session.commit()

    print('Done! Database seeded successfully.')
    print('Test accounts:')
    print('  username: john_doe   | password: password123')
    print('  username: jane_smith | password: password456')
