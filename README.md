# Productivity Notes App

A simple Flask API for managing personal notes.

## Installation

1. Install dependencies: `pipenv install`
2. Run the seed script to create the database and add sample data: `python seed.py`

## Run Instructions

Run the app with: `python app.py`

## Endpoints

- GET /notes - Retrieve list of notes
- POST /notes - Create a new note (body: {title, content})
- PATCH /notes/<id> - Update a note (body: {title, content})
- DELETE /notes/<id> - Delete a note