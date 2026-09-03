from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from issue_tracker.Errors.admin_error import AdminError
from issue_tracker.Errors.issue_error import IssueError
from issue_tracker.Errors.user_error import UserError


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = []

    for error in exc.errors():
        errors.append(
            {
                "field": error["loc"][-1],
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Invalid request data",
            "errors": errors,
        },
    )


async def user_error_handler(request: Request, exc: UserError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


async def admin_error_handler(request: Request, exc: AdminError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


async def issue_error_handler(request: Request, exc: IssueError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
