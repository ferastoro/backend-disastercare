from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Supply(Base):
    __tablename__ = "supplies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum("makanan", "obat", "tenda", "pakaian", "lainnya"), nullable=False)
    unit = Column(String(20), nullable=False)
    quantity_available = Column(Integer, default=0)
    description = Column(Text)

    # relasi
    allocations = relationship("Allocation", back_populates="supply")