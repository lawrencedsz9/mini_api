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

@app.post("/users")
def create_user(user:User):
    if user.id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users[user.id]= user.model_dump()
    return {"message":"User created successfully"}