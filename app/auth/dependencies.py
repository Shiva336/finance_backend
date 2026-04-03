from fastapi import Depends, HTTPException, Request, status
import jwt

from app.auth.security import decode_token
from app.repositories.user_repo import user_repo
from app.db.session import get_db

async def get_current_user(request: Request, db=Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Access token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    if payload.get("type") != "access":
        raise HTTPException(401, "Invalid token type")

    user_id = int(payload["sub"])

    user = await user_repo.get_by_id(db, user_id)

    if not user:
        raise HTTPException(401, "User not found")

    if not user.is_active:
        raise HTTPException(403, "Inactive user")

    return user