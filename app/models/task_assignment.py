from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime, default=func.now())
    status = Column(Enum("assigned", "ongoing", "done"), default="assigned")
    notes = Column(Text)

    # relasi
    task = relationship("Task", back_populates="assignments")
    user = relationship("User", back_populates="task_assignments")