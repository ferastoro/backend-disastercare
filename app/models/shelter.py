from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True, index=True)
    disaster_id = Column(Integer, ForeignKey("disasters.id"), nullable=False)

    name = Column(String(150), nullable=False)
    location = Column(String(200), nullable=False)
    capacity = Column(Integer, default=0)
    current_occupancy = Column(Integer, default=0)

    status = Column(
        Enum("aktif", "hampir_penuh", "penuh", "nonaktif"),
        default="aktif",
        nullable=False
    )

    coordinator_name = Column(String(100))
    contact_phone = Column(String(30))
    description = Column(Text)

    created_at = Column(DateTime, default=func.now())

    disaster = relationship("Disaster", back_populates="shelters")
    needs = relationship("ShelterNeed", back_populates="shelter", cascade="all, delete-orphan")