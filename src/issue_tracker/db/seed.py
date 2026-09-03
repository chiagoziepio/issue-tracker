import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import select

from issue_tracker.core.security import Security
from issue_tracker.db.session import AsyncSessionLocal
from issue_tracker.model.user import UserModel, UserRole

load_dotenv()


async def seed_admin_user():
    async with AsyncSessionLocal() as db:
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")
        if not email or not password:
            print("Admin user not configured")
            return
        query = select(UserModel).where(UserModel.email == email)
        result = await db.execute(query)
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            print("Admin user already exists")
            return

        security = Security()
        hashed_password = security.hash_password(password)
        new_admin = UserModel(
            email=email,
            password=hashed_password,
            user_name="system admin",
            is_active=True,
            role=UserRole.ADMIN,
        )
        db.add(new_admin)
        await db.commit()

        print("Admin user created")


async def main() -> None:
    await seed_admin_user()


if __name__ == "__main__":
    asyncio.run(main())
