from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShelterNeedBase(BaseModel):
    shelter_id: int
    item_name: str
    category: str
    quantity: int
    unit: str
    priority: Optional[str] = "sedang"
    status: Optional[str] = "diajukan"
    notes: Optional[str] = None


class ShelterNeedCreate(ShelterNeedBase):
    pass


class ShelterNeedUpdate(BaseModel):
    item_name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class ShelterNeedOut(ShelterNeedBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True