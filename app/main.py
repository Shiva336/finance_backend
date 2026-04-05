from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.users.router import router as user_router
from app.categories.router import router as category_router
from app.records.router import router as record_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/v1/user", tags=["Auth"])
app.include_router(category_router, prefix="/api/categories", tags=["Categories"])
app.include_router(record_router, prefix="/api/records", tags=["Records"])