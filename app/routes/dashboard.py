from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.disaster import Disaster
from app.models.registration import Registration
from app.models.task import Task
from app.models.task_assignment import TaskAssignment
from app.models.supply import Supply
from app.models.report import Report
from app.models.shelter import Shelter
from app.models.shelter_need import ShelterNeed
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    role = current_user.role

    if role == "admin":
        return {
            "role": role,
            "active_disasters": db.query(Disaster).filter(Disaster.end_date == None).count(),
            "reports": db.query(Report).count(),
            "registrations": db.query(Registration).count(),
            "tasks": db.query(Task).count(),
            "supplies": db.query(Supply).count(),
            "shelters": db.query(Shelter).count(),
            "critical_needs": db.query(ShelterNeed).filter(ShelterNeed.priority == "kritis").count(),
        }

    if role == "koordinator":
        return {
            "role": role,
            "active_disasters": db.query(Disaster).filter(Disaster.end_date == None).count(),
            "pending_registrations": db.query(Registration).filter(Registration.status == "pending").count(),
            "active_tasks": db.query(Task).filter(Task.status != "done").count(),
            "assignments": db.query(TaskAssignment).count(),
            "critical_needs": db.query(ShelterNeed).filter(ShelterNeed.priority == "kritis").count(),
            "supplies": db.query(Supply).count(),
            "reports": db.query(Report).count(),
        }

    return {
        "role": role,
        "my_registrations": db.query(Registration).filter(Registration.user_id == current_user.id).count(),
        "my_assignments": db.query(TaskAssignment).filter(TaskAssignment.user_id == current_user.id).count(),
        "my_reports": db.query(Report).filter(Report.reported_by == current_user.id).count(),
        "active_disasters": db.query(Disaster).filter(Disaster.end_date == None).count(),
    }