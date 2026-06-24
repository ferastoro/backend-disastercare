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
    region = Column(String(150))
    readiness = Column(
        Enum("aktif", "siaga", "tidak_tersedia"),
        default="aktif"
    )
    availability = Column(String(150))
    transport = Column(String(100))
    area = Column(String(200))
    emergency_contact = Column(String(150))
    profile_photo = Column(String(255))
    
    # relasi
    registrations = relationship("Registration", back_populates="user")
    task_assignments = relationship("TaskAssignment", back_populates="user")
    reports = relationship("Report", foreign_keys="[Report.reported_by]", back_populates="reporter")
    skills = relationship("VolunteerSkill", back_populates="user", cascade="all, delete-orphan")