from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class RegistrationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

# Saat relawan daftar, cukup kirim disaster_id + notes
# user_id diambil otomatis dari token, bukan dari body
class RegistrationCreate(BaseModel):
    disaster_id: int
    notes: Optional[str] = None

# Hanya admin/koordinator yang bisa ubah status
class RegistrationUpdate(BaseModel):
    status: RegistrationStatus
    notes: Optional[str] = None

class RegistrationOut(BaseModel):
    id: int
    user_id: int
    disaster_id: int
    registered_at: datetime
    status: RegistrationStatus
    notes: Optional[str] = None

    class Config:
        from_attributes = True