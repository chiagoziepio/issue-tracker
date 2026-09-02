from pydantic import BaseModel, ConfigDict


class BasicResponse(BaseModel):
    message: str
    status_code: int
    model_config = ConfigDict(from_attributes=True)
