from pydantic import BaseModel, ConfigDict

from issue_tracker.model.issues_model import IssueStatus
from issue_tracker.schemas.response_schema import BasicResponse


class IssueResponse(BaseModel):
    id: str
    title: str
    description: str
    status: IssueStatus
    user_id: str

    model_config = ConfigDict(from_attributes=True)


class GetIssuesResquest(BaseModel):
    page: int | None = None
    limit: int | None = None
    search: str | None = None
    status: IssueStatus | None = None

    model_config = ConfigDict(from_attributes=True)


class GetIssuesResponse(BasicResponse):
    issues: list[IssueResponse]
    total_count: int
    model_config = ConfigDict(from_attributes=True)
