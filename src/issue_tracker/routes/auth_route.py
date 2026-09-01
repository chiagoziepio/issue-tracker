from fastapi import APIRouter, HTTPException, status

from issue_tracker.db.session import Db_session
from issue_tracker.Errors.user_error import UserError
from issue_tracker.schemas.user_schema import UserCreate, UserResponse
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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
