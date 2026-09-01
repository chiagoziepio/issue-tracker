import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    # Enforces minimum length out of the box
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        # 1. Check for lowercase letters
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")

        # 2. Check for uppercase letters
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")

        # 3. Check for digits
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")

        # 4. Check for special characters (common symbols)
        if not re.search(r"[@$!%*?&_#^()-+=|[\]{}~:;<>./?]", value):
            raise ValueError("Password must contain at least one special character.")

        return value

    user_name: str = Field(min_length=3, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: str
    email: str
    user_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
