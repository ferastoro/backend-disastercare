from pydantic import BaseModel
from datetime import datetime


class VolunteerSkillCreate(BaseModel):
    skill_name: str


class VolunteerSkillOut(BaseModel):
    id: int
    user_id: int
    skill_name: str
    created_at: datetime

    class Config:
        from_attributes = True