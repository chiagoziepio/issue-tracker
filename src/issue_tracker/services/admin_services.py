from sqlalchemy.ext.asyncio import AsyncSession

from issue_tracker.Errors.admin_error import AdminError
from issue_tracker.repositories.admin_repository import AdminRepository


class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.admin_repo = AdminRepository(db)

    async def get_all_admins(self):
        """Fetches all admins from the database."""
        try:
            admins, total_count = await self.admin_repo._get_all_admins()
            return admins, total_count
        except Exception as e:  # noqa
            raise AdminError(f"An error occurred while fetching all admins: {e!s}")
