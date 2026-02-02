from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel

app = FastAPI()

users = {
    2003: {"id":2003, "name":"lawrence"},
    2004:{"id":2004, "name":"john"}
}

class User(BaseModel):
    id:int
    name:str

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
    
    users[user.id]= user.dict()
    return users