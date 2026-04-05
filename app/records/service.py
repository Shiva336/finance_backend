from fastapi import HTTPException
from app.repositories.record_repo import record_repo

class RecordService:
    async def create(self, db, user, data):
        data_dict = data.dict()
        data_dict["user_id"] = user.id
        return await record_repo.create(db, data_dict)

    async def list(self, db, user, filters, page, limit):
        offset = (page - 1) * limit
        return await record_repo.get_filtered(db, filters, user.id, limit, offset)

    async def update(self, db, user, record_id, data):
        record = await record_repo.get_by_id(db, record_id)

        if not record or record.user_id != user.id:
            raise HTTPException(404, "Record not found")

        return await record_repo.update(db, record, data.dict(exclude_unset=True))

    async def delete(self, db, user, record_id):
        record = await record_repo.get_by_id(db, record_id)

        if not record or record.user_id != user.id:
            raise HTTPException(404, "Record not found")

        await record_repo.soft_delete(db, record)

record_service = RecordService()