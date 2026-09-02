from sqlalchemy.ext.asyncio import AsyncSession

from issue_tracker.Errors.issue_error import IssueError
from issue_tracker.repositories.issues_repository import IssuesRepository
from issue_tracker.schemas.issues_schema import GetIssuesResquest


class IssuesService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.issues_repo = IssuesRepository(db)

    async def get_a_particular_user_issues(
        self, user_id: str, query_data: GetIssuesResquest
    ):
        """Fetches a user's issues from the database."""
        try:
            issues, total_count = await self.issues_repo.get_a_user_issues(
                user_id, query_data
            )
            return issues, total_count

        except Exception as e:  # noqa
            raise IssueError(
                f"An error occurred while fetching the user's issues: {e!s}"
            )
