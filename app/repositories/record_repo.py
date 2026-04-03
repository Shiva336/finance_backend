from sqlalchemy import select, and_
from app.models.financial_record import FinancialRecord

class RecordRepo:
    async def create(self, db, data):
        record = FinancialRecord(**data)
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record

    async def get_filtered(self, db, filters, user_id, limit, offset):
        query = select(FinancialRecord).where(
            FinancialRecord.user_id == user_id,
            FinancialRecord.is_deleted == False
        )

        if filters.get("type"):
            query = query.where(FinancialRecord.type == filters["type"])

        if filters.get("category_id"):
            query = query.where(FinancialRecord.category_id == filters["category_id"])

        if filters.get("start_date"):
            query = query.where(FinancialRecord.date >= filters["start_date"])

        if filters.get("end_date"):
            query = query.where(FinancialRecord.date <= filters["end_date"])

        query = query.offset(offset).limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, db, record_id):
        result = await db.execute(
            select(FinancialRecord).where(FinancialRecord.id == record_id)
        )
        return result.scalar_one_or_none()

    async def update(self, db, record, data):
        for key, value in data.items():
            setattr(record, key, value)
        await db.commit()
        return record

    async def soft_delete(self, db, record):
        record.is_deleted = True
        await db.commit()
        
record_repo: RecordRepo = RecordRepo()