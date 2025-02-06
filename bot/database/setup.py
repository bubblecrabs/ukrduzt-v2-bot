from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession

from bot.config import Config
from bot.database.base import Base

config = Config()

async_engine: AsyncEngine = create_async_engine(config.postgres.url, echo=False)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=async_engine)


async def async_init_db() -> None:
    """Initialize the database by creating all tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
