# Mini API

A FastAPI application with JWT authentication, SQLAlchemy ORM, and task management.

## Project Structure

```
mini_api/
├── __init__.py                 # Root package initialization
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── app/
    ├── __init__.py            
    ├── main.py                # FastAPI routes and app initialization
    ├── auth.py                # Authentication utilities and JWT handling
    ├── config.py              # Centralized configuration (env vars)
    ├── db.py                  # Database engine and session setup
    ├── dependencies.py        # Shared dependencies (DB sessions)
    ├── models.py              # SQLAlchemy ORM models
    └── schemas.py             # Pydantic request/response schemas
```

## Features

- **User Management**: Create users with secure PBKDF2-SHA256 password hashing
- **JWT Authentication**: OAuth2-compatible token-based authentication with Swagger UI integration
- **Task Management**: Full CRUD operations for user-scoped tasks
- **Database Support**: SQLite (local) and PostgreSQL (production)
- **Environment-aware**: Auto-switches between local and production configurations

##1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn app.main:app --reload
```

The app will be available at **http://localhost:8000**
  ```json
  {"name": "username", "password": "password"}
  ```
- `POST /login` - Get JWT access token (form data)
  - Use Swagger UI's **Authorize** button for easy testing
- `GET /me` - Get current user info **(protected)**

### Tasks
- `GET /tasks` - List user's tasks **(protected)**
- `POST /tasks` - Create a new task **(protected)**
  ```json
  {"title": "Task title"}
  ```
- `PUT /tasks/{task_id}` - Update a task **(protected)**
  ```json
  {"title": "Updated title", "completed": true}
  ```
- `DELETE /tasks/{task_id}` - Delete a task **(protected)**

## Security

- **Password Hashing**: PBKDF2-SHA256 
- **JWT Tokens**: HS256 algorithm with configurable expiration
- **Protected Routes**: OAuth2 Bearer token required
- **User Isolation**: Users only see their own tasks

## Deployment

Quick summary:
1. Create PostgreSQL database on Render
2. Create Web Service connected to GitHub repo
3. Set environment variables
4. Deploy

## Testing Endpoints Locally

```powershell
# Create user
Invoke-RestMethod -Uri http://localhost:8000/users -Method Post `
  -Body (@{name="testuser"; password="testpass123"} | ConvertTo-Json) `
  -ContentType "application/json"

# Login
$response = Invoke-RestMethod -Uri http://localhost:8000/login -Method Post `
  -Body @{username="testuser"; password="testpass123"}
$token = $response.access_token

# Get current user
Invoke-RestMethod http://localhost:8000/me `
  -Headers @{Authorization = "Bearer $token"}

# Create task
Invoke-RestMethod -Uri http://localhost:8000/tasks -Method Post `
  -Headers @{Authorization = "Bearer $token"} `
  -Body (@{title="My first task"} | ConvertTo-Json) `
  -ContentType "application/json"
```

## Technology Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib (PBKDF2-SHA256)
- **Database**: SQLite (local) / PostgreSQL (production or via Render Hosting)
- **Server**: Uvicorn



**Hosting via Render:**
- PostgreSQL managed by Render
- Connection via `DATABASE_URL` environment variable

## Environment Variables

All environment variables are optional locally (falls back to sensible defaults).

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `DATABASE_URL` | No (local) | SQLite at `app.db` | Database connection string |
| `SECRET_KEY` | No (local) | Dev key | JWT signing secret (50+ chars for production) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | JWT token expiration time |

**For local development:** Just run the server, everything works out of the box.

**For production:** Set all three variables in your Render environment settings.
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
