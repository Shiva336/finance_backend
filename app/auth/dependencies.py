from fastapi import Depends, HTTPException, Request
import jwt

from app.auth.security import decode_token
from app.repositories.user_repo import UserRepo
from app.db.session import get_db

user_repo = UserRepo()

async def get_current_user(request: Request, db=Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(401, "Not authenticated")

    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")

    if payload["type"] != "access":
        raise HTTPException(401, "Invalid token")

    user = await user_repo.get_by_id(db, int(payload["sub"]))
    if not user:
        raise HTTPException(401, "User not found")

    return user