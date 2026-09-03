from pydantic import BaseModel, ConfigDict

from issue_tracker.schemas.response_schema import BasicResponse


class AdminResponse(BaseModel):
    id: str
    email: str
    user_name: str
    is_active: bool
    role: str
    model_config = ConfigDict(from_attributes=True)


class GetAllAdminsResponse(BasicResponse):
    admins: list[AdminResponse]
    total_count: int
    model_config = ConfigDict(from_attributes=True)
