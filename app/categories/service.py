from app.repositories.category_repo import category_repo

class CategoryService:
    async def create(self, db, data):
        return await category_repo.create(db, data)

    async def list(self, db):
        return await category_repo.get_all(db)


category_service = CategoryService()