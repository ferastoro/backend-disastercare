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

    # Profil tambahan untuk kebutuhan frontend DisasterCare
    region = Column(String(150))
    readiness = Column(
        Enum("aktif", "siaga", "tidak_tersedia"),
        default="aktif",
    )
    availability = Column(String(150))
    transport = Column(String(100))
    area = Column(String(200))
    emergency_contact = Column(String(150))
    profile_photo = Column(String(255))

    # Relasi pendaftaran bencana
    registrations = relationship(
        "Registration",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Relasi assignment tugas
    task_assignments = relationship(
        "TaskAssignment",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Relasi laporan yang dibuat user.
    # WAJIB pakai foreign_keys karena reports punya 2 FK ke users:
    # reported_by dan reviewed_by.
    reports = relationship(
        "Report",
        back_populates="reporter",
        foreign_keys="Report.reported_by",
        cascade="all, delete-orphan",
    )

    # Relasi laporan yang direview oleh admin/koordinator.
    reviewed_reports = relationship(
        "Report",
        back_populates="reviewer",
        foreign_keys="Report.reviewed_by",
    )

    # Relasi skill relawan
    skills = relationship(
        "VolunteerSkill",
        back_populates="user",
        cascade="all, delete-orphan",
    )