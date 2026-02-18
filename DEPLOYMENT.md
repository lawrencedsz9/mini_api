# Deployment Guide for Render

This guide explains how to deploy your mini_api project to Render with PostgreSQL.

## 📋 Changes Made for Production

### 1. **Centralized Configuration** (`app/config.py`)

**What changed:**
- Created a new `config.py` file to manage all environment variables
- `SECRET_KEY`: Used for JWT token signing (falls back to dev key locally)
- `DATABASE_URL`: Supports both SQLite (local) and PostgreSQL (production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Configurable token expiry (default: 30 minutes)

**Why it's needed:**
- No hardcoded secrets in code
- Easy switching between local and production environments
- Follows 12-factor app methodology

### 2. **Database Configuration** (`app/db.py`)

**What changed:**
- Now reads `DATABASE_URL` from environment variables (via config)
- Automatically detects SQLite vs PostgreSQL
- Only applies `check_same_thread=False` for SQLite (not needed for PostgreSQL)

**Why it's needed:**
- Render provides PostgreSQL via `DATABASE_URL` environment variable
- SQLite is not suitable for production (file-based, not persistent in cloud)
- PostgreSQL is production-ready and scalable

### 3. **Authentication Configuration** (`app/auth.py`)

**What changed:**
- Imports `SECRET_KEY`, `ALGORITHM`, and `ACCESS_TOKEN_EXPIRE_MINUTES` from config
- No more hardcoded values

**Why it's needed:**
- Each deployment should have a unique SECRET_KEY
- Token expiry can be configured per environment

### 4. **Dependencies** (`requirements.txt`)

**What changed:**
- Added `psycopg2-binary` - PostgreSQL adapter for Python

**Why it's needed:**
- SQLAlchemy needs this driver to connect to PostgreSQL

---

## 🧪 Testing Locally Before Deployment

### 1. **Test with SQLite (Current Setup)**

Your existing setup should work exactly as before:

```powershell
# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

**Test all endpoints:**
1. `POST /users` - Create a user
2. `POST /login` - Login and get token
3. `GET /me` - Verify token works
4. `POST /tasks` - Create task (with token)
5. `GET /tasks` - List tasks (with token)
6. `PUT /tasks/{id}` - Update task (with token)
7. `DELETE /tasks/{id}` - Delete task (with token)

### 2. **Test with PostgreSQL Locally** (Optional but Recommended)

Install PostgreSQL locally and test with it:

```powershell
# Set environment variables
$env:DATABASE_URL = "postgresql://user:password@localhost/mini_api_db"
$env:SECRET_KEY = "your-test-secret-key-here-make-it-long-and-random"

# Run the server
uvicorn app.main:app --reload
```

Repeat all the endpoint tests above to ensure everything works with PostgreSQL.

---

## 🚀 Deploying to Render

### Step 1: Create PostgreSQL Database

1. Log in to [Render](https://render.com)
2. Click **New +** → **PostgreSQL**
3. Configure:
   - **Name**: `mini-api-db` (or your choice)
   - **Database**: `mini_api`
   - **User**: (auto-generated)
   - **Region**: Choose closest to your users
   - **Plan**: Free tier is fine for testing
4. Click **Create Database**
5. **Important**: Copy the **Internal Database URL** (starts with `postgresql://`)

### Step 2: Create Web Service

1. Click **New +** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `mini-api` (or your choice)
   - **Environment**: `Python 3`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables

In the **Environment** section of your web service, add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Paste the Internal Database URL from your PostgreSQL instance |
| `SECRET_KEY` | Generate a random secret (use a password generator, 50+ characters) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` (or your preferred value) |

**To generate a secure SECRET_KEY:**

```powershell
# Run this in PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | ForEach-Object {[char]$_})
```

### Step 4: Deploy

1. Click **Create Web Service**
2. Render will automatically build and deploy your app
3. Database tables will be created automatically on first run
4. Your API will be available at: `https://your-service-name.onrender.com`

---

## ✅ Verification Checklist

After deployment, test these endpoints (replace `YOUR_URL` with your Render URL):

```powershell
# 1. Test root endpoint
curl https://YOUR_URL.onrender.com/

# 2. Create a user
curl -X POST https://YOUR_URL.onrender.com/users `
  -H "Content-Type: application/json" `
  -d '{"name": "testuser", "password": "testpass123"}'

# 3. Login
$response = curl -X POST https://YOUR_URL.onrender.com/login `
  -H "Content-Type: application/json" `
  -d '{"name": "testuser", "password": "testpass123"}' | ConvertFrom-Json

$token = $response.access_token

# 4. Test protected endpoint
curl https://YOUR_URL.onrender.com/me `
  -H "Authorization: Bearer $token"

# 5. Create a task
curl -X POST https://YOUR_URL.onrender.com/tasks `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{"title": "Test task from production"}'
```

---

## 🔐 Security Notes

1. **Never commit your production SECRET_KEY to Git**
   - It's in environment variables only
   - The dev key in `config.py` is just a fallback for local development

2. **DATABASE_URL is provided by Render**
   - Render automatically sets this when you link a PostgreSQL database
   - You can also set it manually in environment variables

3. **HTTPS is automatic**
   - Render provides free SSL certificates
   - All traffic is encrypted

---

## 🐛 Troubleshooting

### Database connection errors

**Issue**: `could not connect to server`
- **Fix**: Make sure you're using the **Internal Database URL** from Render, not the external one
- Check that your web service and database are in the same region

### JWT token errors

**Issue**: `Invalid token` or `signature verification failed`
- **Fix**: Ensure `SECRET_KEY` environment variable is set on Render
- Make sure it's a long, random string

### Import errors

**Issue**: `ModuleNotFoundError`
- **Fix**: Ensure all dependencies are in `requirements.txt`
- Check build logs on Render to see if installation failed

### Tables don't exist

**Issue**: `no such table: users`
- **Fix**: The app automatically creates tables on startup via `Base.metadata.create_all(bind=engine)`
- Check that your database URL is correct
- Restart the web service on Render

---

## 📊 Local vs Production Differences

| Aspect | Local Development | Production (Render) |
|--------|-------------------|---------------------|
| **Database** | SQLite (file: `app.db`) | PostgreSQL (managed by Render) |
| **DATABASE_URL** | Not set (falls back to SQLite) | Set by Render |
| **SECRET_KEY** | Dev fallback key | Unique production secret |
| **Port** | 8000 (default) | Dynamic via `$PORT` env var |
| **HTTPS** | Not enabled | Automatic SSL/TLS |
| **Persistence** | File on disk | PostgreSQL cluster |

---

## 🎯 What Wasn't Changed

✅ **API behavior is identical**
- All routes work the same way
- Request/response formats unchanged
- Authentication logic unchanged

✅ **Database models unchanged**
- All SQLAlchemy models remain the same
- Relationships and constraints intact

✅ **No new features added**
- Only infrastructure changes for production readiness

---

## 🔄 Next Steps (Optional)

Consider these improvements for production:

1. **Add CORS middleware** (if building a frontend)
2. **Add request rate limiting** (prevent abuse)
3. **Add logging** (for debugging production issues)
4. **Add health check endpoint** (for monitoring)
5. **Add database migrations** (using Alembic for schema changes)

These are NOT required for initial deployment but can be added later as needed.
