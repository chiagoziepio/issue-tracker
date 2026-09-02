from fastapi import APIRouter, HTTPException, Response, status

from issue_tracker.core.config import get_config
from issue_tracker.db.session import Db_session
from issue_tracker.Errors.user_error import UserError
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
    """Authenticate a user and return an access token."""
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
        return UserResponse.model_validate(auth_response.user)
    except UserError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
