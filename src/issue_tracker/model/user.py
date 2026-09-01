from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column

from issue_tracker.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        unique=True,
        index=True,
        doc="The user's id",
        server_default=text("(hex(randomblob(16)))"),
    )
    email: Mapped[str] = mapped_column(
        String(255),
        doc="The user's email",
        unique=True,
        index=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        doc="The user's password",
        nullable=False,
    )
    user_name: Mapped[str] = mapped_column(doc="The user's name", nullable=False)
    is_active: Mapped[bool] = mapped_column(
        doc="Whether the user is active",
        nullable=False,
        default=True,
    )
