from sqlalchemy import Column, Integer, ForeignKey, Date, Text, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    disaster_id = Column(Integer, ForeignKey("disasters.id"), nullable=False)

    # User yang membuat laporan
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    report_date = Column(Date, nullable=False)
    content = Column(Text, nullable=False)
    attachments = Column(String(255))
    created_at = Column(DateTime, default=func.now())

    # Field tambahan untuk validasi laporan
    status = Column(String(30), default="submitted", nullable=False)
    priority = Column(String(30), default="sedang", nullable=False)
    review_notes = Column(Text)

    # User admin/koordinator yang mereview laporan
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    reviewed_at = Column(DateTime)

    # Relasi ke bencana
    disaster = relationship(
        "Disaster",
        back_populates="reports",
    )

    # Relasi ke user pembuat laporan.
    # WAJIB foreign_keys supaya SQLAlchemy tidak bingung.
    reporter = relationship(
        "User",
        back_populates="reports",
        foreign_keys=[reported_by],
    )

    # Relasi ke user reviewer laporan.
    # WAJIB foreign_keys karena users juga terhubung lewat reported_by.
    reviewer = relationship(
        "User",
        back_populates="reviewed_reports",
        foreign_keys=[reviewed_by],
    )