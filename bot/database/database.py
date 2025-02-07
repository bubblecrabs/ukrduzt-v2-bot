from sqlalchemy import select, func, desc, insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.database.models.user import User
from bot.core.config import settings

async_engine = create_async_engine(settings.postgres.url, echo=False)
async_session = async_sessionmaker(bind=async_engine)


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


async def get_user_is_admin(user_id: int) -> bool:
    """Check if the user is an admin."""
    async with async_session() as session:
        stmt = select(User.is_admin).filter_by(user_id=user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def add_user(user_id: int, username: str | None) -> User:
    """Add a new user to the database and return the user."""
    async with async_session() as session:
        stmt = insert(User).values(user_id=user_id, username=username)
        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one_or_none()


async def update_user(user_id: int, faculty: int, course: int, group: int, group_name: str) -> User:
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
        return user
