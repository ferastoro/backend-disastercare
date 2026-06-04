from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    disaster_id = Column(Integer, ForeignKey("disasters.id"), nullable=False)
    title = Column(String(200), nullable=False)
    category = Column(Enum("evakuasi", "logistik", "medis", "komunikasi", "lainnya"), nullable=False)
    status = Column(Enum("open", "ongoing", "done"), default="open")
    max_volunteers = Column(Integer)
    location = Column(String(200))

    # relasi
    disaster = relationship("Disaster", back_populates="tasks")
    assignments = relationship("TaskAssignment", back_populates="task")