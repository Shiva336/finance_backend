from fastapi import APIRouter, Depends
from app.categories.schemas import CategoryCreate, CategoryResponse
from app.categories.service import category_service
from app.db.session import get_db
from app.auth.permissions import require_roles

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
async def create_category(
    data: CategoryCreate,
    db=Depends(get_db),
    user=Depends(require_roles(["admin"]))
):
    return await category_service.create(db, data)


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(db=Depends(get_db)):
    return await category_service.list(db)