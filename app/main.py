from fastapi import FastAPI, Depends
from app.auth.router import router as auth_router
from app.users.router import router as user_router
from app.categories.router import router as category_router
from app.records.router import router as record_router
from app.dashboard.router import router as dashboard_router
from app.core.rate_limiter import global_rate_limit

app = FastAPI(dependencies=[Depends(global_rate_limit)])

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(category_router, prefix="/api/categories", tags=["Categories"])
app.include_router(record_router, prefix="/api/records", tags=["Records"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])