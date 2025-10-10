# Social Media API – User Auth Setup

## Setup Instructions

1. Clone the repo and navigate into it.
2. Install dependencies: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Run server: `python manage.py runserver`

## User Endpoints

- `POST /api/auth/register/` – Register new user (returns token)
- `POST /api/auth/login/` – Login with credentials (returns token)
- `GET /api/auth/profile/` – View or update profile (requires auth token)

## User Model

- Fields: `username`, `email`, `bio`, `profile_picture`, `followers`
