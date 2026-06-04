from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.registration import Registration
from app.models.disaster import Disaster
from app.schemas.registration import RegistrationCreate, RegistrationUpdate, RegistrationOut
from app.core.dependencies import get_current_user, require_role
from typing import List
from datetime import date

router = APIRouter(prefix="/registrations", tags=["Registrations"])

# Relawan daftar ke bencana
# user_id diambil dari token, bukan dari request body
@router.post("/", response_model=RegistrationOut)
def register_to_disaster(
    payload: RegistrationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("relawan", "koordinator"))
):
    # Cek disaster-nya ada dulu
    disaster = db.query(Disaster).filter(Disaster.id == payload.disaster_id).first()
    if not disaster:
        raise HTTPException(status_code=404, detail="Disaster not found")

    if disaster.end_date and disaster.end_date < date.today():
        raise HTTPException(status_code=400, detail="Pendaftaran ditolak: Kejadian bencana ini sudah berakhir.")

    # Cek kalau udah pernah daftar ke bencana yang sama
    existing = db.query(Registration).filter(
        Registration.user_id == current_user.id,
        Registration.disaster_id == payload.disaster_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already registered to this disaster")

    registration = Registration(
        user_id=current_user.id,  # dari token
        disaster_id=payload.disaster_id,
        notes=payload.notes
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

# Relawan lihat registrasi milik mereka sendiri
@router.get("/me", response_model=List[RegistrationOut])
def get_my_registrations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Registration).filter(
        Registration.user_id == current_user.id
    ).all()

# Admin/koordinator lihat semua registrasi
@router.get("/", response_model=List[RegistrationOut])
def get_all_registrations(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    return db.query(Registration).all()

# Admin/koordinator approve atau reject
@router.put("/{registration_id}", response_model=RegistrationOut)
def update_registration_status(
    registration_id: int,
    payload: RegistrationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    registration = db.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(registration, field, value)

    db.commit()
    db.refresh(registration)
    return registration