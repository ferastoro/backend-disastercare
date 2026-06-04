from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class DisasterType(str, Enum):
    gempa = "gempa"
    banjir = "banjir"
    longsor = "longsor"
    tsunami = "tsunami"
    kebakaran = "kebakaran"
    lainnya = "lainnya"

class EmergencyLevel(str, Enum):
    rendah = "rendah"
    sedang = "sedang"
    tinggi = "tinggi"
    kritis = "kritis"

class DisasterCreate(BaseModel):
    title: str
    location: str
    type: DisasterType
    emergency_level: EmergencyLevel
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class DisasterUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    type: Optional[DisasterType] = None
    emergency_level: Optional[EmergencyLevel] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None

class DisasterOut(BaseModel):
    id: int
    title: str
    location: str
    type: DisasterType
    emergency_level: EmergencyLevel
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True