from fastapi import APIRouter, Depends, Response, Request
from app.auth.service import auth_service
from app.auth.schemas import LoginRequest, RegisterRequest
from app.db.session import get_db
from app.core.config import settings
from app.core.cookies import set_auth_cookies, clear_auth_cookies

router = APIRouter(prefix="/api/auth")

@router.post("/register")
async def register(data: RegisterRequest, response: Response, db=Depends(get_db)):
    user, access, refresh = await auth_service.register(db, data.email, data.password)
    set_auth_cookies(response, access, refresh)
    return {"user": user.email}

@router.post("/login")
async def login(data: LoginRequest, response: Response, db=Depends(get_db)):
    user, access, refresh = await auth_service.login(db, data.email, data.password)
    set_auth_cookies(response, access, refresh)
    return {"user": user.email}

@router.post("/refresh")
async def refresh(request: Request, response: Response, db=Depends(get_db)):
    token = request.cookies.get("refresh_token")
    access, refresh = await auth_service.refresh(db, token)
    set_auth_cookies(response, access, refresh)
    return {"message": "refreshed"}

@router.post("/logout")
async def logout(request: Request, response: Response, db=Depends(get_db)):
    token = request.cookies.get("refresh_token")
    await auth_service.logout(db, token)
    clear_auth_cookies(response)
    return {"message": "logged out"}