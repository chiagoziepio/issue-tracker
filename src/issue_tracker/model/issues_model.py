from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from issue_tracker.db.base import Base

if TYPE_CHECKING:
    from issue_tracker.model.user import UserModel


class IssueStatus(StrEnum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    REOPENED = "REOPENED"
    DELETED = "DELETED"


class IssueModel(Base):
    __tablename__ = "issues"
    id: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        unique=True,
        index=True,
        doc="The issue's id",
        default=lambda: uuid4().hex.upper(),
    )
    title: Mapped[str] = mapped_column(doc="The issue's title", nullable=False)
    description: Mapped[str] = mapped_column(
        doc="The issue's description", nullable=False
    )
    status: Mapped[IssueStatus] = mapped_column(
        doc="The issue's status", nullable=False, default=IssueStatus.OPEN
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        doc="The issue's user id",
        index=True,
        nullable=True,
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="issues", doc="The issue's user"
    )
