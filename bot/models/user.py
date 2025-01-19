from sqlalchemy import Integer, BigInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.base import Base

class User(Base):
    """Represents a user in the system."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    user_faculty: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_course: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_group: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_group_name: Mapped[str | None] = mapped_column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", name="unique_user_id"),
        UniqueConstraint("username", name="unique_username"),
    )
