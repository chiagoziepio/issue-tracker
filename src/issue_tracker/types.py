from typing import TypedDict


class ACCESS_TOKEN_COOKIE_DATA_TYPE(TypedDict):
    user_id: str
    type: str


class REFRESH_TOKEN_COOKIE_DATA_TYPE(TypedDict):
    user_id: str
    type: str


class COOKIE_TOKENS(TypedDict):
    access_token: str
    refresh_token: str
