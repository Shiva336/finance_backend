from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.users.router import router as user_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/v1/user", tags=["Auth"])