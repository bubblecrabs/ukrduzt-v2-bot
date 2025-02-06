from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.core.config import Config
from bot.database.models.base import Base

config = Config()

async_engine = create_async_engine(config.postgres.url, echo=False)
async_session = async_sessionmaker(bind=async_engine)


async def async_init_db() -> None:
    """Initialize the database by creating all tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
