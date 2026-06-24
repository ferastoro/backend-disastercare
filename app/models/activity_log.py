from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    role_target = Column(String(30))
    title = Column(String(150), nullable=False)
    description = Column(Text)
    type = Column(String(50), default="info")
    is_read = Column(Integer, default=0)

    created_at = Column(DateTime, default=func.now())