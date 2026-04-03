from fastapi import Depends, HTTPException, status
from typing import List

from app.auth.dependencies import get_current_user


def require_roles(allowed_roles: List[str]):
    """
    Dependency factory for role-based access control.

    Usage:
        Depends(require_roles(["admin"]))
    """

    async def role_checker(user=Depends(get_current_user)):
        if user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return role_checker