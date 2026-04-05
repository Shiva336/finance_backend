from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RecordCreate(BaseModel):
    amount: float
    type: str
    category_id: int
    date: datetime
    notes: Optional[str] = None


class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    category_id: Optional[int] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None


class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category_id: int
    date: datetime
    notes: Optional[str]

    model_config = {"from_attributes": True}