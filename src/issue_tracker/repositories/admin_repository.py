from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from issue_tracker.model.user import UserModel


class AdminRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_all_admins(self):
        query = select(UserModel).where(UserModel.role == "ADMIN")

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.db.execute(count_query)
        total_count = count_result.scalar_one()

        query = query.order_by(UserModel.id.desc())
        result = await self.db.execute(query)

        admins = list(result.scalars().all())
        return admins, total_count
