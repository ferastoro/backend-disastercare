from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ReportCreate(BaseModel):
    disaster_id: int
    report_date: date
    content: str
    attachments: Optional[str] = None

class ReportUpdate(BaseModel):
    report_date: Optional[date] = None
    content: Optional[str] = None
    attachments: Optional[str] = None

class ReportOut(BaseModel):
    id: int
    disaster_id: int
    reported_by: int
    report_date: date
    content: str
    attachments: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
