from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatusEnum = TaskStatusEnum.pending

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
