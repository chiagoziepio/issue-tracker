from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi import Security as FastAPISecurity
from fastapi.security import APIKeyCookie
from jwt import InvalidTokenError

from issue_tracker.core.security import Security
from issue_tracker.db.session import Db_session
from issue_tracker.Errors.user_error import UserError
from issue_tracker.model.user import UserModel
from issue_tracker.repositories.user_repository import UserRepository
from issue_tracker.types import (
    ACCESS_TOKEN_COOKIE_DATA_TYPE,
    REFRESH_TOKEN_COOKIE_DATA_TYPE,
)

access_token_cookie = APIKeyCookie(name="access_token", auto_error=False)
refresh_token_cookie = APIKeyCookie(name="refresh_token", auto_error=False)


async def get_access_token_cookie_data(
    access_token: Annotated[str | None, FastAPISecurity(access_token_cookie)],
) -> ACCESS_TOKEN_COOKIE_DATA_TYPE:
    """Dependency to retrieve and verify the access token from cookies."""
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    security = Security()
    try:
        payload = security.verify_access_token(access_token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return payload


ACCESS_TOKEN_DEP = Annotated[
    ACCESS_TOKEN_COOKIE_DATA_TYPE, Depends(get_access_token_cookie_data)
]


async def get_current_user(access_token: ACCESS_TOKEN_DEP, db: Db_session) -> UserModel:
    """Dependency to retrieve the current user from the database."""
    user_repo = UserRepository(db)
    try:
        user = await user_repo.get_user_by_id(access_token["user_id"])
        if not user:
            raise UserError(
                status_code=status.HTTP_404_NOT_FOUND, message="User not found"
            )
    except UserError as e:
        raise UserError(message=str(e.message), status_code=e.status_code)
    except Exception as e:  # noqa
        raise UserError(message=f"An error occurred while fetching the user: {e!s}")
    return user


CURRENT_USER_DEP = Annotated[UserModel, Depends(get_current_user)]


async def get_fresh_token_cookie_data(
    refresh_token: Annotated[str | None, FastAPISecurity(refresh_token_cookie)],
) -> REFRESH_TOKEN_COOKIE_DATA_TYPE:
    """Dependency to retrieve and verify the refresh token from cookies."""
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    security = Security()
    try:
        payload = security.verify_fresh_token(refresh_token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return payload


REFRESH_TOKEN_DEP = Annotated[
    REFRESH_TOKEN_COOKIE_DATA_TYPE, Depends(get_fresh_token_cookie_data)
]


async def get_current_user_from_refresh_token(
    refresh_token: REFRESH_TOKEN_DEP, db: Db_session
) -> UserModel:
    """Dependency to retrieve the current user from the database."""
    user_repo = UserRepository(db)
    try:
        user = await user_repo.get_user_by_id(refresh_token["user_id"])
        if not user:
            raise UserError(
                status_code=status.HTTP_404_NOT_FOUND, message="User not found"
            )
    except UserError as e:
        raise UserError(message=str(e.message), status_code=e.status_code)
    except Exception as e:  # noqa
        raise UserError(message=f"An error occurred while fetching the user: {e!s}")
    return user


CURRENT_USER_FROM_REFRESH_TOKEN_DEP = Annotated[
    UserModel, Depends(get_current_user_from_refresh_token)
]
