from fastapi import HTTPException, status
import jwt

from app.auth.security import *
from app.repositories.user_repo import user_repo
from app.repositories.token_repo import token_repo

class AuthService:

    async def register(self, db, email, password):
        existing = await user_repo.get_by_email(db, email)
        if existing:
            raise HTTPException(400, "Email already registered")

        hashed = hash_password(password)
        user = await user_repo.create(db, email, hashed)

        access = create_access_token(user.id)
        refresh, jti, exp = create_refresh_token(user.id)

        await token_repo.create(db, user.id, jti, exp)

        return user, access, refresh


    async def login(self, db, email, password):
        user = await user_repo.get_by_email(db, email)

        if not user or not verify_password(password, user.password_hashed):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

        access = create_access_token(user.id)
        refresh, jti, exp = create_refresh_token(user.id)

        await token_repo.create(db, user.id, jti, exp)

        return user, access, refresh


    async def refresh(self, db, token: str):
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Refresh token expired")

        if payload["type"] != "refresh":
            raise HTTPException(401, "Invalid token")

        jti = payload["jti"]

        stored = await token_repo.get(db, jti)
        if not stored:
            raise HTTPException(401, "Token revoked")

        user_id = int(payload["sub"])

        # rotate
        await token_repo.revoke(db, jti)

        access = create_access_token(user_id)
        new_refresh, new_jti, exp = create_refresh_token(user_id)

        await token_repo.create(db, user_id, new_jti, exp)

        return access, new_refresh


    async def logout(self, db, token: str):
        payload = decode_token(token)
        await token_repo.revoke(db, payload["jti"])


auth_service = AuthService()