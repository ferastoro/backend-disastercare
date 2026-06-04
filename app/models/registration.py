from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    disaster_id = Column(Integer, ForeignKey("disasters.id"), nullable=False)
    registered_at = Column(DateTime, default=func.now())
    status = Column(Enum("pending", "approved", "rejected"), default="pending")
    notes = Column(Text)

    # relasi
    user = relationship("User", back_populates="registrations")
    disaster = relationship("Disaster", back_populates="registrations")