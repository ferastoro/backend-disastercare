from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.disaster import Disaster
from app.schemas.disaster import DisasterCreate, DisasterUpdate, DisasterOut
from app.core.dependencies import get_current_user, require_role
from typing import List

router = APIRouter(prefix="/disasters", tags=["Disasters"])

# Semua user login bisa lihat
@router.get("/", response_model=List[DisasterOut])
def get_all_disasters(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Disaster).all()

@router.get("/{disaster_id}", response_model=DisasterOut)
def get_disaster(
    disaster_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    disaster = db.query(Disaster).filter(Disaster.id == disaster_id).first()
    if not disaster:
        raise HTTPException(status_code=404, detail="Disaster not found")
    return disaster

# Admin only untuk write operations
@router.post("/", response_model=DisasterOut)
def create_disaster(
    payload: DisasterCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    disaster = Disaster(**payload.model_dump())
    db.add(disaster)
    db.commit()
    db.refresh(disaster)
    return disaster

@router.put("/{disaster_id}", response_model=DisasterOut)
def update_disaster(
    disaster_id: int,
    payload: DisasterUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    disaster = db.query(Disaster).filter(Disaster.id == disaster_id).first()
    if not disaster:
        raise HTTPException(status_code=404, detail="Disaster not found")
    
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(disaster, field, value)
    
    db.commit()
    db.refresh(disaster)
    return disaster

@router.delete("/{disaster_id}")
def delete_disaster(
    disaster_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    disaster = db.query(Disaster).filter(Disaster.id == disaster_id).first()
    if not disaster:
        raise HTTPException(status_code=404, detail="Disaster not found")
    
    db.delete(disaster)
    db.commit()
    return {"message": f"Disaster '{disaster.title}' deleted"}