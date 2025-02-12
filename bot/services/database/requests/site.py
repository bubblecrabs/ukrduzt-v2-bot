from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.database.models.site import WebsiteSettings


async def set_year_and_semester(session: AsyncSession) -> None:
    """Creates default settings if not exists."""
    stmt = insert(WebsiteSettings).values(id=1, year=81, semester=2).on_conflict_do_nothing(index_elements=["id"])
    await session.execute(stmt)
    await session.commit()


async def get_website_settings(session: AsyncSession) -> WebsiteSettings:
    """Get site settings from the database."""
    stmt = select(WebsiteSettings).where(WebsiteSettings.id == 1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_year(session: AsyncSession, year: int) -> None:
    """Updates the year value in the WebsiteSettings table."""
    stmt = update(WebsiteSettings).where(WebsiteSettings.id == 1).values(year=year)
    await session.execute(stmt)
    await session.commit()


async def update_semester(session: AsyncSession, semester: int) -> None:
    """Updates the semester value in the WebsiteSettings table."""
    stmt = update(WebsiteSettings).where(WebsiteSettings.id == 1).values(semester=semester)
    await session.execute(stmt)
    await session.commit()
