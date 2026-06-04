from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.models.task_assignment import TaskAssignment
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.schemas.task_assignment import TaskAssignmentCreate, TaskAssignmentUpdate, TaskAssignmentOut, AssignmentStatus
from app.core.dependencies import get_current_user, require_role
from typing import List

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# ─── TASK CRUD ─────────────────────────────────────────────

# Semua user bisa lihat task yang tersedia
@router.get("/", response_model=List[TaskOut])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Task).all()

@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Hanya admin/koordinator yang bisa buat dan kelola task
@router.post("/", response_model=TaskOut)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": f"Task '{task.title}' deleted"}


# ─── TASK ASSIGNMENTS ──────────────────────────────────────

# Relawan ambil/daftarkan diri ke task
@router.post("/{task_id}/assign", response_model=TaskAssignmentOut)
def assign_to_task(
    task_id: int,
    payload: TaskAssignmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("relawan", "koordinator"))
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Task yang sudah 'done' tidak bisa diambil lagi
    if task.status == "done":
        raise HTTPException(status_code=400, detail="Task is already done")

    # Cek kuota relawan kalau max_volunteers diset
    if task.max_volunteers:
        current_count = db.query(TaskAssignment).filter(
            TaskAssignment.task_id == task_id
        ).count()
        if current_count >= task.max_volunteers:
            raise HTTPException(status_code=400, detail="Task is already full")

    # Cek kalau sudah pernah assign ke task yang sama
    existing = db.query(TaskAssignment).filter(
        TaskAssignment.task_id == task_id,
        TaskAssignment.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already assigned to this task")

    assignment = TaskAssignment(
        task_id=task_id,
        user_id=current_user.id,  # dari token
        notes=payload.notes
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

# Relawan lihat task yang sedang mereka kerjakan
@router.get("/assignments/me", response_model=List[TaskAssignmentOut])
def get_my_assignments(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(TaskAssignment).filter(
        TaskAssignment.user_id == current_user.id
    ).all()

# Admin/koordinator lihat semua assignment
@router.get("/assignments/all", response_model=List[TaskAssignmentOut])
def get_all_assignments(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    return db.query(TaskAssignment).all()

# Admin/koordinator update status assignment (ongoing/done)
@router.put("/assignments/{assignment_id}", response_model=TaskAssignmentOut)
def update_assignment(
    assignment_id: int,
    payload: TaskAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    assignment = db.query(TaskAssignment).filter(TaskAssignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(assignment, field, value)

    db.commit()
    db.refresh(assignment)
    return assignment

@router.put("/assignments/me/{assignment_id}/status", response_model=TaskAssignmentOut)
def update_my_assignment_status(
    assignment_id: int,
    status: AssignmentStatus,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("relawan", "koordinator"))
):
    # CEK IDOR: Pastikan user_id pada assignment sama dengan current_user.id
    assignment = db.query(TaskAssignment).filter(
        TaskAssignment.id == assignment_id,
        TaskAssignment.user_id == current_user.id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found or you don't own this assignment")

    assignment.status = status
    db.commit()
    db.refresh(assignment)
    return assignment