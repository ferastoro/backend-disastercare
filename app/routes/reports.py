from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.report import Report
from app.models.disaster import Disaster
from app.schemas.report import ReportCreate, ReportUpdate, ReportOut
from app.core.dependencies import get_current_user, require_role
from typing import List

router = APIRouter(prefix="/reports", tags=["Reports"])

# Semua user login bisa melihat laporan
@router.get("/", response_model=List[ReportOut])
def get_all_reports(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Report).all()

# Melihat laporan per bencana
@router.get("/disaster/{disaster_id}", response_model=List[ReportOut])
def get_reports_by_disaster(
    disaster_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Report).filter(Report.disaster_id == disaster_id).all()

@router.get("/{report_id}", response_model=ReportOut)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

# Siapapun yang login bisa buat report
@router.post("/", response_model=ReportOut)
def create_report(
    payload: ReportCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    disaster = db.query(Disaster).filter(Disaster.id == payload.disaster_id).first()
    if not disaster:
        raise HTTPException(status_code=404, detail="Disaster not found")

    report = Report(
        disaster_id=payload.disaster_id,
        reported_by=current_user.id,
        report_date=payload.report_date,
        content=payload.content,
        attachments=payload.attachments
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

# Bisa update asal yang buat report atau admin/koordinator
@router.put("/{report_id}", response_model=ReportOut)
def update_report(
    report_id: int,
    payload: ReportUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.reported_by != current_user.id and current_user.role not in ["admin", "koordinator"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this report")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(report, field, value)

    db.commit()
    db.refresh(report)
    return report

# Hanya admin yang bisa menghapus laporan sepenuhnya
@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()
    return {"message": "Report deleted"}
