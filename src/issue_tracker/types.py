from typing import TypedDict

from issue_tracker.model.issues_model import IssueStatus


class ACCESS_TOKEN_COOKIE_DATA_TYPE(TypedDict):
    user_id: str
    type: str


class REFRESH_TOKEN_COOKIE_DATA_TYPE(TypedDict):
    user_id: str
    type: str


class COOKIE_TOKENS(TypedDict):
    access_token: str
    refresh_token: str


class ISSUES_PAGINATION(TypedDict):
    page: int | None
    limit: int | None
    search: str | None
    status: IssueStatus | None
