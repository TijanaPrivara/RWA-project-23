from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class PriorityEnum(str, Enum):
    low = "low"
    regular = "regular"
    high = "high"

class ProjectIn(BaseModel):
    name: str
    description: str

class ProjectDb(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str

class TaskIn(BaseModel):
    title: str
    description: str
    priority: PriorityEnum
    status: str
    due_date: datetime
    project_name: str

class TaskDb(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str
    priority: str
    status: str
    due_date: datetime
    project_name: str

class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserDb(BaseModel):
    username: str = Field(alias="_id")
    email: str
    hashed_password: str