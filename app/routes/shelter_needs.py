from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.shelter import Shelter
from app.models.shelter_need import ShelterNeed
from app.schemas.shelter_need import ShelterNeedCreate, ShelterNeedUpdate, ShelterNeedOut
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/shelter-needs", tags=["Shelter Needs"])


@router.get("/", response_model=List[ShelterNeedOut])
def get_all_shelter_needs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(ShelterNeed).all()


@router.get("/shelter/{shelter_id}", response_model=List[ShelterNeedOut])
def get_shelter_needs_by_shelter(
    shelter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(ShelterNeed).filter(ShelterNeed.shelter_id == shelter_id).all()


@router.post("/", response_model=ShelterNeedOut)
def create_shelter_need(
    payload: ShelterNeedCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "koordinator"))
):
    shelter = db.query(Shelter).filter(Shelter.id == payload.shelter_id).first()

    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    need = ShelterNeed(**payload.model_dump())

    db.add(need)
    db.commit()
    db.refresh(need)

    return need


@router.put("/{need_id}", response_model=ShelterNeedOut)
def update_shelter_need(
    need_id: int,
    payload: ShelterNeedUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "koordinator"))
):
    need = db.query(ShelterNeed).filter(ShelterNeed.id == need_id).first()

    if not need:
        raise HTTPException(status_code=404, detail="Shelter need not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(need, field, value)

    db.commit()
    db.refresh(need)

    return need


@router.delete("/{need_id}")
def delete_shelter_need(
    need_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "koordinator"))
):
    need = db.query(ShelterNeed).filter(ShelterNeed.id == need_id).first()

    if not need:
        raise HTTPException(status_code=404, detail="Shelter need not found")

    db.delete(need)
    db.commit()

    return {"message": "Shelter need deleted"}