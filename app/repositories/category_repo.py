from sqlalchemy import select
from app.models.category import Category

class CategoryRepo:
    async def create(self, db, data):
        category = Category(**data.dict())
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    async def get_all(self, db):
        result = await db.execute(select(Category))
        return result.scalars().all()
    
category_repo: CategoryRepo = CategoryRepo()