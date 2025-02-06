from sqlalchemy import select, func, desc

from bot.database.session import async_session
from bot.database.models.user import User


async def get_user_by_id(user_id: int) -> User | None:
    """Fetch a single user by their unique user_id."""
    async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def get_users_count() -> int:
    """Get the total count of users in the database."""
    async with async_session() as session:
        stmt = select(func.count()).select_from(User)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def get_latest_user() -> User | None:
    """Get the most recently created user based on ID."""
    async with async_session() as session:
        stmt = select(User).order_by(desc(User.id)).limit(1)
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


async def update_user(user_id: int, faculty: int, course: int, group: int, group_name: str) -> None:
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
