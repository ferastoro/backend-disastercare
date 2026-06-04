from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class AssignmentStatus(str, Enum):
    assigned = "assigned"
    ongoing = "ongoing"
    done = "done"

# Relawan cukup kirim task_id, user_id dari token
class TaskAssignmentCreate(BaseModel):
    task_id: int
    notes: Optional[str] = None

class TaskAssignmentUpdate(BaseModel):
    status: AssignmentStatus
    notes: Optional[str] = None

class TaskAssignmentOut(BaseModel):
    id: int
    task_id: int
    user_id: int
    assigned_at: datetime
    status: AssignmentStatus
    notes: Optional[str] = None

    class Config:
        from_attributes = True