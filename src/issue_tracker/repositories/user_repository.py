from typing import TypedDict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from issue_tracker.model.user import UserModel


class UserData(TypedDict):
    email: str
    password: str
    user_name: str


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> UserModel | None:
        """Fetches a user from the database matching the provided email."""
        query = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def save_user_to_db(self, user_data: UserData) -> UserModel:
        """Saves a new user to the database."""
        new_user = UserModel(
            email=user_data.get("email"),
            password=user_data.get("password"),
            user_name=user_data.get("user_name"),
            is_active=True,
        )
        self.db.add(new_user)
        await self.db.flush()  # Populates the auto-generated string ID
        return new_user
