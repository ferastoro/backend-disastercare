from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SupplyCategory(str, Enum):
    makanan = "makanan"
    obat = "obat"
    tenda = "tenda"
    pakaian = "pakaian"
    lainnya = "lainnya"

class SupplyCreate(BaseModel):
    name: str
    category: SupplyCategory
    unit: str
    quantity_available: int = 0
    description: Optional[str] = None

class SupplyUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[SupplyCategory] = None
    unit: Optional[str] = None
    quantity_available: Optional[int] = None
    description: Optional[str] = None

class SupplyOut(BaseModel):
    id: int
    name: str
    category: SupplyCategory
    unit: str
    quantity_available: int
    description: Optional[str] = None

    class Config:
        from_attributes = True