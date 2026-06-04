from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("relawan", "koordinator", "admin"), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime, default=func.now())

    # relasi
    registrations = relationship("Registration", back_populates="user")
    task_assignments = relationship("TaskAssignment", back_populates="user")
    reports = relationship("Report", back_populates="reporter")