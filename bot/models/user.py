from datetime import datetime
from sqlalchemy import Integer, BigInteger, String, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.base import Base

class User(Base):
    """Represents a user in the system."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(35), unique=True, nullable=True)
    user_faculty: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_course: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_group: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_group_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", name="unique_user_id"),
        UniqueConstraint("username", name="unique_username"),
    )
