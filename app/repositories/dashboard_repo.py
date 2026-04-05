from sqlalchemy import select, func, case
from sqlalchemy.orm import aliased
from app.models.financial_record import FinancialRecord
from app.models.category import Category

class DashboardRepo:
    async def summary(self, db, user_id):
        result = await db.execute(
            select(
                func.sum(
                    case(
                        (FinancialRecord.type == "income", FinancialRecord.amount),
                        else_=0
                    )
                ).label("income"),
                func.sum(
                    case(
                        (FinancialRecord.type == "expense", FinancialRecord.amount),
                        else_=0
                    )
                ).label("expense"),
            ).where(
                FinancialRecord.user_id == user_id,
                FinancialRecord.is_deleted == False
            )
        )

        row = result.one()

        income = row.income or 0
        expense = row.expense or 0

        return {
            "total_income": float(income),
            "total_expense": float(expense),
            "net_balance": float(income - expense)
        }


    async def category_breakdown(self, db, user_id):
        result = await db.execute(
            select(
                Category.name,
                func.sum(FinancialRecord.amount)
            )
            .join(Category, FinancialRecord.category_id == Category.id)
            .where(
                FinancialRecord.user_id == user_id,
                FinancialRecord.is_deleted == False
            )
            .group_by(Category.name)
        )

        return [
            {"category": row[0], "total": float(row[1])}
            for row in result.all()
        ]


    async def monthly_trends(self, db, user_id):
        month_expr = func.date_trunc('month', FinancialRecord.date)

        result = await db.execute(
            select(
                month_expr.label("month"),
                func.sum(
                    case(
                        (FinancialRecord.type == "income", FinancialRecord.amount),
                        else_=0
                    )
                ).label("income"),
                func.sum(
                    case(
                        (FinancialRecord.type == "expense", FinancialRecord.amount),
                        else_=0
                    )
                ).label("expense"),
            )
            .where(
                FinancialRecord.user_id == user_id,
                FinancialRecord.is_deleted == False
            )
            .group_by(month_expr)
            .order_by(month_expr)
        )

        return [
            {
                # format AFTER grouping ✅
                "month": row.month.strftime("%Y-%m"),
                "income": float(row.income or 0),
                "expense": float(row.expense or 0),
            }
            for row in result.all()
        ]


    async def recent_activity(self, db, user_id):
        result = await db.execute(
            select(
                FinancialRecord.id,
                FinancialRecord.amount,
                FinancialRecord.type,
                Category.name
            )
            .join(Category, FinancialRecord.category_id == Category.id)
            .where(
                FinancialRecord.user_id == user_id,
                FinancialRecord.is_deleted == False
            )
            .order_by(FinancialRecord.created_at.desc())
            .limit(5)
        )

        return [
            {
                "id": row[0],
                "amount": float(row[1]),
                "type": row[2],
                "category": row[3],
            }
            for row in result.all()
        ]
        
dashboard_repo: DashboardRepo = DashboardRepo()