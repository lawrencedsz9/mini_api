# Mini API

A structured FastAPI application with JWT authentication and task management.

## Project Structure

```
mini_api/
├── __init__.py                 # Root package initialization
├── README.md                   # Project documentation
└── app/
    ├── __init__.py            # App package initialization
    ├── main.py                # FastAPI app and route definitions
    ├── auth.py                # Authentication utilities and JWT handling
    ├── db.py                  # Database configuration and engine setup
    ├── dependencies.py        # Shared dependencies (e.g., database sessions)
    ├── models.py              # SQLAlchemy ORM models
    └── schemas.py             # Pydantic schemas for request/response validation
```

## Features

- **User Management**: Create users with password hashing
- **JWT Authentication**: Secure token-based authentication
- **Task Management**: CRUD operations for user-specific tasks
- **Database**: SQLite with SQLAlchemy ORM

## Running the Application

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the server
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /users` - Create a new user
- `POST /login` - Login and get access token
- `GET /me` - Get current user info (protected)

### Tasks
- `GET /tasks` - Get all tasks for the current user (protected)
- `POST /tasks` - Create a new task (protected)
- `PUT /tasks/{task_id}` - Update a task (protected)
- `DELETE /tasks/{task_id}` - Delete a task (protected)
