from fastapi import APIRouter, Depends, HTTPException, status

from issue_tracker.db.session import Db_session
from issue_tracker.deps.user_auth_deps import require_role
from issue_tracker.Errors.admin_error import AdminError
from issue_tracker.model.user import UserRole
from issue_tracker.schemas.admin_schema import AdminResponse, GetAllAdminsResponse
from issue_tracker.services.admin_services import AdminService

router = APIRouter(
    tags=["Admin"],
    prefix="/admin",
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=GetAllAdminsResponse,
)
async def get_all_admins(db: Db_session) -> GetAllAdminsResponse:
    """Get all admins."""
    admin_service = AdminService(db)
    try:
        admins, total_count = await admin_service.get_all_admins()
        return GetAllAdminsResponse(
            message="Admins retrieved successfully",
            status_code=status.HTTP_200_OK,
            admins=list(map(AdminResponse.model_validate, admins)),
            total_count=total_count,
        )
    except AdminError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:  # noqa
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
