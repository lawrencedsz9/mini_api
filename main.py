from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import engine, Base, SessionLocal
from models import UserDB, TaskDB

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ---------- Pydantic Schemas ----------

class User(BaseModel):
    id: int
    name: str

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
    user_id: int

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
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

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()
    return tasks

@app.get("/users/{user_id}/tasks")
def get_tasks_for_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.tasks


@app.post("/tasks")
def create_task(task: Task, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == task.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_task = TaskDB(
        id=task.id,
        title=task.title,
        completed=task.completed,
        user_id=task.user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created successfully", "task": new_task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

@app.put("/tasks/{task_id}/toggle")
def toggle_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    db.commit()
    db.refresh(task)

    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.title is not None:
        db_task.title = task.title
    if task.completed is not None:
        db_task.completed = task.completed

    db.commit()
    db.refresh(db_task)

    return db_task

