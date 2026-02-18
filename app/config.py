import os
from pathlib import Path

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Database Configuration
# For local development: SQLite
# For production: PostgreSQL via DATABASE_URL environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'app.db'}"
)

# JWT Configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-in-production-12345678901234567890"
)

# Token expiry in minutes (default: 30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# JWT Algorithm
ALGORITHM = "HS256"
