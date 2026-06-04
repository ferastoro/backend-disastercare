from sqlalchemy import Column, Integer, String, Enum, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Disaster(Base):
    __tablename__ = "disasters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    type = Column(Enum("gempa", "banjir", "longsor", "tsunami", "kebakaran", "lainnya"), nullable=False)
    emergency_level = Column(Enum("rendah", "sedang", "tinggi", "kritis"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(Text)

    # relasi
    tasks = relationship("Task", back_populates="disaster", cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="disaster", cascade="all, delete-orphan")
    allocations = relationship("Allocation", back_populates="disaster", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="disaster", cascade="all, delete-orphan")