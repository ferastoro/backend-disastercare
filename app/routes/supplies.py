from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.supply import Supply
from app.models.allocation import Allocation
from app.models.disaster import Disaster
from app.schemas.supply import SupplyCreate, SupplyUpdate, SupplyOut
from app.schemas.allocation import AllocationCreate, AllocationOut
from app.core.dependencies import get_current_user, require_role
from typing import List

router = APIRouter(prefix="/supplies", tags=["Supplies"])

# ─── SUPPLY CRUD ───────────────────────────────────────────

# Semua user bisa lihat stok logistik
@router.get("/", response_model=List[SupplyOut])
def get_all_supplies(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Supply).all()

@router.get("/{supply_id}", response_model=SupplyOut)
def get_supply(
    supply_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    supply = db.query(Supply).filter(Supply.id == supply_id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")
    return supply

# Admin/koordinator kelola inventaris
@router.post("/", response_model=SupplyOut)
def create_supply(
    payload: SupplyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    supply = Supply(**payload.model_dump())
    db.add(supply)
    db.commit()
    db.refresh(supply)
    return supply

@router.put("/{supply_id}", response_model=SupplyOut)
def update_supply(
    supply_id: int,
    payload: SupplyUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    supply = db.query(Supply).filter(Supply.id == supply_id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(supply, field, value)

    db.commit()
    db.refresh(supply)
    return supply

@router.delete("/{supply_id}")
def delete_supply(
    supply_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    supply = db.query(Supply).filter(Supply.id == supply_id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")

    db.delete(supply)
    db.commit()
    return {"message": f"Supply '{supply.name}' deleted"}


# ─── ALLOCATIONS ───────────────────────────────────────────

# Lihat semua alokasi logistik
@router.get("/allocations/all", response_model=List[AllocationOut])
def get_all_allocations(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    return db.query(Allocation).all()

# Lihat alokasi per bencana tertentu
@router.get("/allocations/disaster/{disaster_id}", response_model=List[AllocationOut])
def get_allocations_by_disaster(
    disaster_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Allocation).filter(
        Allocation.disaster_id == disaster_id
    ).all()

# Alokasikan logistik ke bencana
# Di sini ada business logic: stok harus dikurangi setelah dialokasikan
@router.post("/allocations", response_model=AllocationOut)
def create_allocation(
    payload: AllocationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin", "koordinator"))
):
    # Cek supply ada
    supply = db.query(Supply).filter(Supply.id == payload.supply_id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Supply not found")

    # Cek disaster ada
    disaster = db.query(Disaster).filter(Disaster.id == payload.disaster_id).first()
    if not disaster:
        raise HTTPException(status_code=404, detail="Disaster not found")

    # Cek stok cukup — tidak boleh alokasi melebihi stok yang ada
    if payload.quantity > supply.quantity_available:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock. Available: {supply.quantity_available} {supply.unit}"
        )

    # Kurangi stok supply setelah dialokasikan
    supply.quantity_available -= payload.quantity

    allocation = Allocation(**payload.model_dump())
    db.add(allocation)
    db.commit()
    db.refresh(allocation)
    return allocation