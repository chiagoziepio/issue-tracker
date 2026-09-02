from fastapi import APIRouter, HTTPException, status

from issue_tracker.deps.user_auth_deps import CURRENT_USER_DEP
from issue_tracker.Errors.user_error import UserError
from issue_tracker.schemas.user_schema import UserProfile, UserResponse

router = APIRouter(
    tags=["User Profile"],
    prefix="/user-profile",
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserProfile)
async def get_current_user_profile(current_user: CURRENT_USER_DEP) -> UserProfile:
    """Get the current user's profile."""
    try:
        user = UserResponse.model_validate(current_user)
        return UserProfile(
            message="User profile retrieved successfully",
            status_code=status.HTTP_200_OK,
            user=user,
        )
    except UserError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
