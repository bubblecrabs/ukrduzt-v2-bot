from collections.abc import Sequence

from sqlalchemy import select, func, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.database.models.user import User


async def get_users(session: AsyncSession) -> Sequence[User]:
    """Fetch all users from the database."""
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    """Fetch a single user by their unique user_id."""
    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_users_count(session: AsyncSession) -> int:
    """Get the total count of users in the database."""
    stmt = select(func.count()).select_from(User)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_latest_user(session: AsyncSession) -> User:
    """Get the most recently created user based on ID."""
    stmt = select(User).order_by(desc(User.id)).limit(1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_is_admin(session: AsyncSession, user_id: int) -> bool:
    """Check if the user is an admin."""
    stmt = select(User.is_admin).filter_by(user_id=user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def add_user(session: AsyncSession, user_id: int, username: str | None) -> None:
    """Add a new user to the database and return the user."""
    stmt = insert(User).values(user_id=user_id, username=username).on_conflict_do_nothing()
    await session.execute(stmt)
    await session.commit()


async def update_user(
        session: AsyncSession,
        user_id: int,
        faculty: int,
        course: int,
        group: int,
        group_name: str
) -> None:
    """Update user information if the user exists."""
    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        user.user_faculty = faculty
        user.user_course = course
        user.user_group = group
        user.user_group_name = group_name
        await session.commit()
