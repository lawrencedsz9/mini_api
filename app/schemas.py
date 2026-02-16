from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class TaskCreate(BaseModel):
    title: str   # ✅ user_id REMOVED


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

    model_config = {
        "from_attributes": True
    }


class LoginRequest(BaseModel):
    name: str
    password: str