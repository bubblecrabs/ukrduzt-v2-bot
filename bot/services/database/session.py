from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession

from bot.core.config import settings


def get_async_engine(url: str) -> AsyncEngine:
    return create_async_engine(url, echo=False)


def get_session_maker(async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=async_engine)


engine = get_async_engine(url=settings.postgres.url)
session_maker = get_session_maker(engine)
