from fastapi import APIRouter, Depends

from app.dashboard.service import dashboard_service
from app.dashboard.schemas import (
    SummaryResponse,
    CategoryBreakdown,
    TrendPoint,
    RecentActivity,
)
from app.db.session import get_db
from app.auth.permissions import require_roles

router = APIRouter()

@router.get("/summary", response_model=SummaryResponse)
async def summary(
    db=Depends(get_db),
    user=Depends(require_roles(["admin", "analyst"]))
):
    return await dashboard_service.get_summary(db, user)


@router.get("/categories", response_model=list[CategoryBreakdown])
async def categories(
    db=Depends(get_db),
    user=Depends(require_roles(["admin", "analyst"]))
):
    return await dashboard_service.get_categories(db, user)


@router.get("/trends", response_model=list[TrendPoint])
async def trends(
    db=Depends(get_db),
    user=Depends(require_roles(["admin", "analyst"]))
):
    return await dashboard_service.get_trends(db, user)


@router.get("/recent", response_model=list[RecentActivity])
async def recent(
    db=Depends(get_db),
    user=Depends(require_roles(["admin", "analyst"]))
):
    return await dashboard_service.get_recent(db, user)