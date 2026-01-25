from fastapi import FastAPI

app = FastAPI()

users = {
    2003: {"id":2003, "name":"lawrence"},
    2004:{"id":2004, "name":"john"}
}

@app.get("/")
def read_root():
    return {"Message": "Backend started"}

@app.get("/users")
def get_users():
    return users