from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ShelterNeed(Base):
    __tablename__ = "shelter_needs"

    id = Column(Integer, primary_key=True, index=True)
    shelter_id = Column(Integer, ForeignKey("shelters.id"), nullable=False)

    item_name = Column(String(120), nullable=False)
    category = Column(
        Enum("makanan", "air", "obat", "pakaian", "tenda", "lainnya"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)
    unit = Column(String(30), nullable=False)

    priority = Column(
        Enum("rendah", "sedang", "tinggi", "kritis"),
        default="sedang",
        nullable=False
    )

    status = Column(
        Enum("diajukan", "diproses", "terpenuhi", "ditolak"),
        default="diajukan",
        nullable=False
    )

    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())

    shelter = relationship("Shelter", back_populates="needs")