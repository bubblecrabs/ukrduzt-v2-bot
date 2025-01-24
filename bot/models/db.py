from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.engine import URL

from bot.config import config

# Generating a URL to connect to the database
url_obj = URL.create(
    drivername="postgresql+asyncpg",
    username=config.postgres_user,
    password=config.postgres_password.get_secret_value(),
    host=config.postgres_host,
    port=5432,
    database=config.postgres_db,
)

# Database engine and session
async_engine: AsyncEngine = create_async_engine(url_obj, echo=False)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=async_engine)

async def async_init_db() -> None:
    """Initialize the database by creating all tables."""
    from .base import Base
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
