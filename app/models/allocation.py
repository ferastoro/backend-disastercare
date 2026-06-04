from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    supply_id = Column(Integer, ForeignKey("supplies.id"), nullable=False)
    disaster_id = Column(Integer, ForeignKey("disasters.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    allocated_at = Column(DateTime, default=func.now())
    allocated_by = Column(String(100))

    # relasi
    supply = relationship("Supply", back_populates="allocations")
    disaster = relationship("Disaster", back_populates="allocations")