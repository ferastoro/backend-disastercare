from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TaskCategory(str, Enum):
    evakuasi = "evakuasi"
    logistik = "logistik"
    medis = "medis"
    komunikasi = "komunikasi"
    lainnya = "lainnya"

class TaskStatus(str, Enum):
    open = "open"
    ongoing = "ongoing"
    done = "done"

class TaskCreate(BaseModel):
    disaster_id: int
    title: str
    category: TaskCategory
    status: Optional[TaskStatus] = TaskStatus.open
    max_volunteers: Optional[int] = None
    location: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[TaskCategory] = None
    status: Optional[TaskStatus] = None
    max_volunteers: Optional[int] = None
    location: Optional[str] = None

class TaskOut(BaseModel):
    id: int
    disaster_id: int
    title: str
    category: TaskCategory
    status: TaskStatus
    max_volunteers: Optional[int] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True