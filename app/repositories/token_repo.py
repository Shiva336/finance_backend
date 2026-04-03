from sqlalchemy import select
from app.models.refresh_token import RefreshToken

class TokenRepo:
    async def create(self, db, user_id, jti, expires_at):
        token = RefreshToken(
            user_id=user_id,
            token_jti=jti,
            expires_at=expires_at
        )
        db.add(token)
        await db.commit()

    async def get(self, db, jti):
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token_jti == jti,
                RefreshToken.revoked == False
            )
        )
        return result.scalar_one_or_none()

    async def revoke(self, db, jti):
        token = await self.get(db, jti)
        if token:
            token.revoked = True
            await db.commit()

token_repo: TokenRepo = TokenRepo()