from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from issue_tracker.db.session import Db_session
from issue_tracker.deps.user_auth_deps import CURRENT_USER_DEP
from issue_tracker.Errors.issue_error import IssueError
from issue_tracker.schemas.issues_schema import (
    BasicResponse,
    GetIssuesResponse,
    GetIssuesResquest,
    GetSingleIssueResponse,
    IssueCreate,
    IssueMutationResponse,
    IssueResponse,
    UpdateIssueDetialsRequest,
    UpdateIssueStatusRequest,
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


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=IssueMutationResponse
)
async def issue_creation(
    issue_data: IssueCreate, current_user: CURRENT_USER_DEP, db: Db_session
) -> IssueMutationResponse:
    """Create a new issue."""
    issue_service = IssuesService(db)
    try:
        new_issue = await issue_service.create_new_issue(current_user.id, issue_data)
        return IssueMutationResponse(
            message="Issue created successfully",
            status_code=status.HTTP_201_CREATED,
            issue=IssueResponse.model_validate(new_issue),
        )
    except IssueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.put(
    "/{issue_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=IssueMutationResponse,
)
async def update_issue_status(
    issue_id: str,
    new_status: UpdateIssueStatusRequest,
    current_user: CURRENT_USER_DEP,
    db: Db_session,
) -> IssueMutationResponse:
    """Update the status of an issue."""

    issue_service = IssuesService(db)

    try:
        issue = await issue_service.update_issue_status(
            current_user.id, issue_id, new_status
        )
        return IssueMutationResponse(
            issue=IssueResponse.model_validate(issue),
            message="Issue status updated successfully",
            status_code=status.HTTP_200_OK,
        )
    except IssueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.put(
    "/{issue_id}/details",
    status_code=status.HTTP_200_OK,
    response_model=IssueMutationResponse,
)
async def update_issue_details(
    issue_id: str,
    issue_data: UpdateIssueDetialsRequest,
    current_user: CURRENT_USER_DEP,
    db: Db_session,
) -> IssueMutationResponse:
    """Update the details of an issue."""

    issue_service = IssuesService(db)

    try:
        issue = await issue_service.update_issue_detials(
            current_user.id, issue_id, issue_data
        )
        return IssueMutationResponse(
            issue=IssueResponse.model_validate(issue),
            message="Issue details updated successfully",
            status_code=status.HTTP_200_OK,
        )
    except IssueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.get(
    "/{issue_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetSingleIssueResponse,
)
async def get_single_issue(
    issue_id: str,
    current_user: CURRENT_USER_DEP,
    db: Db_session,
) -> GetSingleIssueResponse:
    """Get a single issue."""

    issue_service = IssuesService(db)
    try:
        issue = await issue_service.get_issue(current_user.id, issue_id)
        return GetSingleIssueResponse(
            message="Issue retrieved successfully",
            status_code=status.HTTP_200_OK,
            issue=IssueResponse.model_validate(issue),
        )
    except IssueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.delete(
    "/{issue_id}",
    status_code=status.HTTP_200_OK,
    response_model=BasicResponse,
)
async def delete_issue(
    issue_id: str,
    current_user: CURRENT_USER_DEP,
    db: Db_session,
) -> BasicResponse:
    """Delete a single issue."""

    issue_service = IssuesService(db)
    try:
        await issue_service.delete_issue(current_user.id, issue_id)
        return BasicResponse(
            message="Issue deleted successfully",
            status_code=status.HTTP_200_OK,
        )
    except IssueError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
