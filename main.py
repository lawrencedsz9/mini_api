from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import engine, Base, SessionLocal
from models import UserDB

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ---------- Pydantic Schemas ----------

class User(BaseModel):
    id: int
    name: str

# ---------- DB Dependency ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "Backend started"}

@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.id == user.id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = UserDB(id=user.id, name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
