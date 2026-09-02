from fastapi import APIRouter, HTTPException, Response, status

from issue_tracker.core.config import get_config
from issue_tracker.db.session import Db_session
from issue_tracker.deps.user_auth_deps import CURRENT_USER_FROM_REFRESH_TOKEN_DEP
from issue_tracker.Errors.user_error import UserError
from issue_tracker.schemas.response_schema import BasicResponse
from issue_tracker.schemas.user_schema import UserCreate, UserLogin, UserResponse
from issue_tracker.services.auth_services import AuthService

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Db_session):
    """Register a new user in the system."""
    auth_service = AuthService(db)
    try:
        new_user = await auth_service.create_user(user_data)
        return new_user
    except UserError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def login_user(
    login_data: UserLogin, db: Db_session, response: Response
) -> UserResponse:
    """Authenticate a user and set an access token and refresh token cookie."""
    auth_service = AuthService(db)
    try:
        auth_response = await auth_service.authenticate_user(login_data)
        response.set_cookie(
            key="access_token",
            value=auth_response.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=get_config().JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=get_config().JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        response.set_cookie(
            key="refresh_token",
            value=auth_response.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=get_config().JWT_FRESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=get_config().JWT_FRESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return UserResponse.model_validate(auth_response.user)
    except UserError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=BasicResponse)
async def reset_access_token(
    current_user: CURRENT_USER_FROM_REFRESH_TOKEN_DEP,
    db: Db_session,
    response: Response,
) -> BasicResponse:
    """Reset and set a new access token and refresh token cookie using the refresh token."""
    auth_service = AuthService(db)
    try:
        cookies_data = auth_service.generate_cookie_tokens(current_user.id)
        response.set_cookie(
            key="access_token",
            value=cookies_data["access_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=get_config().JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=get_config().JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        response.set_cookie(
            key="refresh_token",
            value=cookies_data["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=get_config().JWT_FRESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=get_config().JWT_FRESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return BasicResponse(
            message="Access token and refresh token cookies reset successfully",
            status_code=status.HTTP_200_OK,
        )
    except UserError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.post("/logout", status_code=status.HTTP_200_OK, response_model=BasicResponse)
async def logout_user(
    response: Response,
) -> BasicResponse:
    """Logout the current user and remove the access token and refresh token cookie."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return BasicResponse(
        message="Access token and refresh token cookies removed successfully",
        status_code=status.HTTP_200_OK,
    )
