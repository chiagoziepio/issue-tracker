# import jwt
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from issue_tracker.Errors.user_error import UserError
from issue_tracker.repositories.user_repository import UserRepository
from issue_tracker.schemas.user_schema import UserCreate, UserResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.password_hash = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    async def create_user(self, user_date: UserCreate) -> UserResponse:
        """Create a new user's account in the system."""

        try:
            already_exists = await self.user_repo.get_user_by_email(user_date.email)
            if already_exists:
                raise UserError("User already exists")

            password = self.hash_password(user_date.password)
            user = await self.user_repo.save_user_to_db(
                user_data={
                    "email": user_date.email,
                    "password": password,
                    "user_name": user_date.user_name,
                }
            )
            await self.db.commit()
            return UserResponse.model_validate(user)
        except UserError as e:
            raise e
        except Exception as e:
            raise UserError(f"An error occurred while creating the user: {e!s}")
