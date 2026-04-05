from app.repositories.dashboard_repo import dashboard_repo

class DashboardService:
    async def get_summary(self, db, user):
        return await dashboard_repo.summary(db, user.id)

    async def get_categories(self, db, user):
        return await dashboard_repo.category_breakdown(db, user.id)

    async def get_trends(self, db, user):
        return await dashboard_repo.monthly_trends(db, user.id)

    async def get_recent(self, db, user):
        return await dashboard_repo.recent_activity(db, user.id)

dashboard_service = DashboardService()