from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from issue_tracker.core.security import Security
from issue_tracker.Errors.user_error import UserError
from issue_tracker.repositories.user_repository import UserRepository
from issue_tracker.schemas.user_schema import (
    AuthenticateUserResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.password_hash = PasswordHash.recommended()
        self.security = Security()

    async def create_user(self, user_date: UserCreate) -> UserResponse:
        """Create a new user's account in the system."""

        try:
            already_exists = await self.user_repo.get_user_by_email(user_date.email)
            if already_exists:
                raise UserError("User already exists")

            password = self.security.hash_password(user_date.password)
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
            raise UserError(e.message, e.status_code)
        except Exception as e:  # noqa
            raise UserError(f"An error occurred while creating the user: {e!s}")

    async def authenticate_user(
        self, login_data: UserLogin
    ) -> AuthenticateUserResponse:
        user = await self.user_repo.get_user_by_email(login_data.email)
        if not user:
            raise UserError("Invalid email or password")

        if not self.security.verify_password(login_data.password, user.password):
            raise UserError("Invalid email or password")
        if not user.is_active:
            raise UserError("User is not active", status_code=403)

        access_token = self.security.generate_access_token(user.id)
        return AuthenticateUserResponse(
            access_token=access_token, user=UserResponse.model_validate(user)
        )
