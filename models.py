from sqlalchemy import Column, Integer, String
from sqlalchemy import Boolean , ForeignKey
from sqlalchemy.orm import relationship

from db import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    tasks = relationship("TaskDB", back_populates="user")

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UserDB", back_populates="tasks")
