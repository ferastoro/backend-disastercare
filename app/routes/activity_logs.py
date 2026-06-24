from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.activity_log import ActivityLog
from app.schemas.activity_log import ActivityLogCreate, ActivityLogOut
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/activity-logs", tags=["Activity Logs"])


@router.get("/", response_model=List[ActivityLogOut])
def get_activity_logs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(ActivityLog).order_by(ActivityLog.created_at.desc()).all()

    return db.query(ActivityLog).filter(
        (ActivityLog.user_id == current_user.id) |
        (ActivityLog.role_target == current_user.role)
    ).order_by(ActivityLog.created_at.desc()).all()


@router.post("/", response_model=ActivityLogOut)
def create_activity_log(
    payload: ActivityLogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "koordinator"))
):
    log = ActivityLog(**payload.model_dump())

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


@router.put("/{log_id}/read", response_model=ActivityLogOut)
def mark_activity_log_as_read(
    log_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    log = db.query(ActivityLog).filter(ActivityLog.id == log_id).first()

    if not log:
        raise HTTPException(status_code=404, detail="Activity log not found")

    log.is_read = 1

    db.commit()
    db.refresh(log)

    return log