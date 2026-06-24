from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.volunteer_skill import VolunteerSkill
from app.schemas.volunteer_skill import VolunteerSkillCreate, VolunteerSkillOut
from app.core.dependencies import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    region: Optional[str] = None
    readiness: Optional[str] = None
    availability: Optional[str] = None
    transport: Optional[str] = None
    area: Optional[str] = None
    emergency_contact: Optional[str] = None
    profile_photo: Optional[str] = None


@router.get("/me")
def get_my_profile(
    current_user=Depends(get_current_user)
):
    return current_user


@router.put("/me")
def update_my_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


@router.put("/me/readiness")
def update_my_readiness(
    readiness: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.readiness = readiness

    db.commit()
    db.refresh(user)

    return user


@router.get("/me/skills", response_model=List[VolunteerSkillOut])
def get_my_skills(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(VolunteerSkill).filter(
        VolunteerSkill.user_id == current_user.id
    ).all()


@router.post("/me/skills", response_model=VolunteerSkillOut)
def add_my_skill(
    payload: VolunteerSkillCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    skill = VolunteerSkill(
        user_id=current_user.id,
        skill_name=payload.skill_name
    )

    db.add(skill)
    db.commit()
    db.refresh(skill)

    return skill


@router.delete("/me/skills/{skill_id}")
def delete_my_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    skill = db.query(VolunteerSkill).filter(
        VolunteerSkill.id == skill_id,
        VolunteerSkill.user_id == current_user.id
    ).first()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()

    return {"message": "Skill deleted"}