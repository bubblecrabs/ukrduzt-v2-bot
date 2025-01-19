from sqlalchemy import Integer, BigInteger, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.engine import URL

from bot.config import config

# Generating a URL to connect to the database
url_obj = URL.create(
    drivername="postgresql+asyncpg",
    username=config.postgres_user,
    password=config.postgres_password.get_secret_value(),
    host=config.postgres_host,
    port=config.postgres_port,
    database=config.postgres_db,
)
# Database engine and session
async_engine: AsyncEngine = create_async_engine(url_obj, echo=False)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=async_engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

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

async def async_init_db() -> None:
    """Initialize the database by creating all tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
