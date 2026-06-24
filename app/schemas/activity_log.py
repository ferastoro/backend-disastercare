from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActivityLogCreate(BaseModel):
    user_id: Optional[int] = None
    role_target: Optional[str] = None
    title: str
    description: Optional[str] = None
    type: Optional[str] = "info"


class ActivityLogOut(ActivityLogCreate):
    id: int
    is_read: int
    created_at: datetime

    class Config:
        from_attributes = True