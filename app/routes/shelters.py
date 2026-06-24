from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.shelter import Shelter
from app.models.disaster import Disaster
from app.schemas.shelter import ShelterCreate, ShelterUpdate, ShelterOut
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/shelters", tags=["Shelters"])


@router.get("/", response_model=List[ShelterOut])
def get_all_shelters(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Shelter).all()


@router.get("/disaster/{disaster_id}", response_model=List[ShelterOut])
def get_shelters_by_disaster(
    disaster_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Shelter).filter(Shelter.disaster_id == disaster_id).all()


@router.get("/{shelter_id}", response_model=ShelterOut)
def get_shelter(
    shelter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    shelter = db.query(Shelter).filter(Shelter.id == shelter_id).first()

    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    return shelter


@router.post("/", response_model=ShelterOut)
def create_shelter(
    payload: ShelterCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "koordinator"))
):
    disaster = db.query(Disaster).filter(Disaster.id == payload.disaster_id).first()

    if not disaster:
        raise HTTPException(status_code=404, detail="Disaster not found")

    shelter = Shelter(**payload.model_dump())

    db.add(shelter)
    db.commit()
    db.refresh(shelter)

    return shelter


@router.put("/{shelter_id}", response_model=ShelterOut)
def update_shelter(
    shelter_id: int,
    payload: ShelterUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "koordinator"))
):
    shelter = db.query(Shelter).filter(Shelter.id == shelter_id).first()

    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(shelter, field, value)

    db.commit()
    db.refresh(shelter)

    return shelter


@router.delete("/{shelter_id}")
def delete_shelter(
    shelter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    shelter = db.query(Shelter).filter(Shelter.id == shelter_id).first()

    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    db.delete(shelter)
    db.commit()

    return {"message": f"Shelter '{shelter.name}' deleted"}