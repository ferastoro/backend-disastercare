from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AllocationCreate(BaseModel):
    supply_id: int
    disaster_id: int
    quantity: int
    allocated_by: Optional[str] = None

class AllocationOut(BaseModel):
    id: int
    supply_id: int
    disaster_id: int
    quantity: int
    allocated_at: datetime
    allocated_by: Optional[str] = None

    class Config:
        from_attributes = True