from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from issue_tracker.db.session import Db_session
from issue_tracker.deps.user_auth_deps import CURRENT_USER_DEP
from issue_tracker.Errors.issue_error import IssueError
from issue_tracker.schemas.issues_schema import (
    GetIssuesResponse,
    GetIssuesResquest,
    IssueResponse,
)
from issue_tracker.services.issues_services import IssuesService

router = APIRouter(tags=["Issues"], prefix="/issues")


@router.get("/", status_code=status.HTTP_200_OK, response_model=GetIssuesResponse)
async def get_user_issues(
    current_user: CURRENT_USER_DEP,
    db: Db_session,
    query_data: Annotated[GetIssuesResquest, Query()],
) -> GetIssuesResponse:
    """Get a user's issues."""

    issue_service = IssuesService(db)
    try:
        issues, total_count = await issue_service.get_a_particular_user_issues(
            current_user.id, query_data
        )
        return GetIssuesResponse(
            message="Issues retrieved successfully",
            status_code=status.HTTP_200_OK,
            issues=list(map(IssueResponse.model_validate, issues)),
            total_count=total_count,
        )
    except IssueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
