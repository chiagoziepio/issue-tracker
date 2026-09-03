from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from issue_tracker.db.base import Base

if TYPE_CHECKING:
    from issue_tracker.model.issues_model import IssueModel


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        unique=True,
        index=True,
        doc="The user's id",
        default=lambda: uuid4().hex.upper(),
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
    issues: Mapped[list["IssueModel"]] = relationship(
        "IssueModel", back_populates="user"
    )
    role: Mapped[UserRole] = mapped_column(
        doc="The user's role",
        nullable=False,
        default=UserRole.USER,
        server_default=UserRole.USER.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
