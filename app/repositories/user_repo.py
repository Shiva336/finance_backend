from sqlalchemy import select
from app.models.user import User

class UserRepo:
    async def get_by_email(self, db, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, db, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db, email: str, password: str):
        user = User(email=email, password_hash=password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
user_repo: UserRepo = UserRepo()