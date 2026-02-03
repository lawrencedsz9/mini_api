from fastapi import FastAPI ,HTTPException 
from pydantic import BaseModel

app = FastAPI()

users = {}

tasks = {}

class User(BaseModel):
    id:int
    name:str

class Task(BaseModel):
    id:int
    title:str
    completed:bool = False
    user_id:int

@app.get("/")
def read_root():
    return {"Message": "Backend started"}

@app.get("/users")
def get_users():
    return users

@app.get("/users/{user_id}")
def get_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    return users[user_id]   

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/users/{user_id}/tasks")
def get_tasks_for_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_tasks = []

    for task in tasks.values():
        if task["user_id"] == user_id:
            user_tasks.append(task)

    if not user_tasks:
        return {"message": "No tasks for this user"}
    
    return user_tasks


@app.post("/users")
def create_user(user:User):
    if user.id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users[user.id]= user.model_dump()
    return {"message":"User created successfully"}

@app.post("/tasks")
def create_task(task:Task):
    if task.id in tasks:
        raise HTTPException(status_code=400, detail="Task already exists")
    
    if task.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    tasks[task.id]= task.model_dump()
    return {"message":"Task created successfully"}