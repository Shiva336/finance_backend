from datetime import datetime, timedelta, timezone
from uuid import uuid4

import bcrypt
import jwt

from app.core.config import settings

_ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=_ALGORITHM)

def create_refresh_token(user_id: int):
    now = datetime.now(timezone.utc)
    jti = uuid4().hex
    exp = now + timedelta(days=settings.refresh_token_expire_days)

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": jti,
        "iat": now,
        "exp": exp,
    }

    token = jwt.encode(payload, settings.secret_key, algorithm=_ALGORITHM)
    return token, jti, exp

def decode_token(token: str):
    return jwt.decode(token, settings.secret_key, algorithms=[_ALGORITHM])