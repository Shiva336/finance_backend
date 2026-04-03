from fastapi import Response
from app.core.config import settings

ACCESS_MAX_AGE = settings.access_token_expire_minutes * 60
REFRESH_MAX_AGE = settings.refresh_token_expire_days * 24 * 60 * 60


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
):
    # Access token → sent everywhere
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=ACCESS_MAX_AGE,
        path="/",
        httponly=settings.cookie_httponly,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
    )

    # Refresh token → ONLY auth routes (security layer)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=REFRESH_MAX_AGE,
        path="/api/auth",
        httponly=settings.cookie_httponly,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
    )


def clear_auth_cookies(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=settings.cookie_httponly,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
    )

    response.delete_cookie(
        key="refresh_token",
        path="/api/auth",
        httponly=settings.cookie_httponly,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
    )