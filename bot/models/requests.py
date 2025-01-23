from collections.abc import Sequence
from sqlalchemy import select, func

from bot.models.db import async_session
from bot.models.user import User


async def db_count_users() -> int:
    """Fetch users and return the total count."""
    async with async_session() as session:
        stmt_count = select(func.count(User.id))
        result_count = await session.execute(stmt_count)
        return result_count.scalar_one()


async def get_users() -> Sequence[User]:
    """Fetch all users from the database."""
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users


async def get_user_by_id(user_id: int) -> User | None:
    """Fetch a single user by their unique user_id."""
    async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def add_user(user_id: int, username: str | None) -> User:
    """Add a new user to the database or update if conflicts exist, and return the user."""
    async with async_session() as session:
        # Check if a user with the given user_id exists
        stmt = select(User).where((User.user_id == user_id))
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            return existing_user

        # Create a new user if no matching user is found
        new_user = User(user_id=user_id, username=username)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def update_user(
    user_id: int,
    faculty: int,
    course: int,
    group: int,
    group_name: str,
) -> None:
    """Update user information if the user exists."""
    async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            user.user_faculty = faculty
            user.user_course = course
            user.user_group = group
            user.user_group_name = group_name
            await session.commit()
