from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShelterBase(BaseModel):
    disaster_id: int
    name: str
    location: str
    capacity: Optional[int] = 0
    current_occupancy: Optional[int] = 0
    status: Optional[str] = "aktif"
    coordinator_name: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None


class ShelterCreate(ShelterBase):
    pass


class ShelterUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    current_occupancy: Optional[int] = None
    status: Optional[str] = None
    coordinator_name: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None


class ShelterOut(ShelterBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True