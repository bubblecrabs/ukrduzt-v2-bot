from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline.schedule import group_kb
from bot.services.database.requests.site import get_website_settings
from bot.services.scraper.scraper import fetch_groups

router = Router()


@router.callback_query(F.data.startswith("course_"))
async def get_group(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Handles the selection of a course."""
    await state.update_data(course=call.data)

    data = await state.get_data()
    faculty = data["faculty"].removeprefix("faculty_")
    course = data["course"].removeprefix("course_")

    site = await get_website_settings(session=session)
    groups = await fetch_groups(faculty=faculty, course=course, year_id=site.year)

    await call.message.edit_text(
        text="Виберіть групу ⬇️",
        reply_markup=await group_kb(groups=groups),
    )
