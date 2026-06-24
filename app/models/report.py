from sqlalchemy import Column, Integer, ForeignKey, Date, Text, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    disaster_id = Column(Integer, ForeignKey("disasters.id"), nullable=False)
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_date = Column(Date, nullable=False)
    content = Column(Text, nullable=False)
    attachments = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    status = Column(
        String(30),
        default="submitted",
        nullable=False
    )

    priority = Column(
        String(30),
        default="sedang",
        nullable=False
    )

    review_notes = Column(Text)
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    reviewed_at = Column(DateTime)

    # relasi
    disaster = relationship("Disaster", back_populates="reports")
    reporter = relationship("User", foreign_keys=[reported_by], back_populates="reports")