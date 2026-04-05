from fastapi import APIRouter, Depends
from app.auth.permissions import require_roles
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
async def get_profile(user=Depends(get_current_user)):
    return user


@router.get("/admin-only")
async def admin_only(user=Depends(require_roles(["admin"]))):
    return {"message": "Only admin allowed"}