from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from issue_tracker.model.issues_model import IssueModel, IssueStatus
from issue_tracker.schemas.issues_schema import GetIssuesResquest, IssueCreate


class IssuesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_a_user_issues(
        self,
        user_id: str,
        query_data: GetIssuesResquest,
    ) -> tuple[list[IssueModel], int]:
        """Fetches a user's issues and the total matching count from the database."""

        query_info = GetIssuesResquest.model_validate(query_data)
        search = query_info.search
        limit = query_info.limit
        page = query_info.page
        status = query_info.status

        query = select(IssueModel).where(IssueModel.user_id == user_id)

        if status:
            query = query.where(IssueModel.status == status)

        if search:
            search_lower = search.lower()
            query = query.where(
                or_(
                    func.lower(IssueModel.title).contains(search_lower),
                    func.lower(IssueModel.description).contains(search_lower),
                )
            )

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.db.execute(count_query)
        total_count = count_result.scalar_one()

        query = query.order_by(IssueModel.id.desc())

        if limit:
            query = query.limit(limit)
            if page and page > 1:
                offset_value = (page - 1) * limit
                query = query.offset(offset_value)

        result = await self.db.execute(query)
        issues = list(result.scalars().all())

        return issues, total_count

    async def create_issue(self, user_id: str, issue_data: IssueCreate) -> IssueModel:
        """Create a new issue in the database."""
        new_issue = IssueModel(
            title=issue_data.title,
            description=issue_data.description,
            status=IssueStatus.OPEN,
            user_id=user_id,
        )
        self.db.add(new_issue)
        await self.db.flush()
        return new_issue
