from fastapi import APIRouter, Depends
from typing import Optional
from datetime import datetime

from app.records.schemas import RecordCreate, RecordResponse, RecordUpdate
from app.records.service import record_service
from app.db.session import get_db
from app.auth.dependencies import get_current_user
from app.auth.permissions import require_roles
# from app.core.rate_limiter import rate_limit

router = APIRouter()

@router.post("/", response_model=RecordResponse)
async def create_record(
    data: RecordCreate,
    db=Depends(get_db),
    user=Depends(require_roles(["admin"]))
):
    return await record_service.create(db, user, data)


@router.get("/", response_model=list[RecordResponse])
async def list_records(
    db=Depends(get_db),
    user=Depends(get_current_user),
    type: Optional[str] = None,
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = 1,
    limit: int = 10,
):
    filters = {
        "type": type,
        "category_id": category_id,
        "start_date": start_date,
        "end_date": end_date,
    }
    return await record_service.list(db, user, filters, page, limit)


@router.patch("/{record_id}", response_model=RecordResponse)
async def update_record(
    record_id: int,
    data: RecordUpdate,
    db=Depends(get_db),
    user=Depends(require_roles(["admin"]))
):
    return await record_service.update(db, user, record_id, data)


@router.delete("/{record_id}")
async def delete_record(
    record_id: int,
    db=Depends(get_db),
    user=Depends(require_roles(["admin"]))
):
    await record_service.delete(db, user, record_id)
    return {"message": "Deleted"}