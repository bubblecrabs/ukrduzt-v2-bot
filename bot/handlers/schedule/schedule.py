from aiogram import F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.database.requests.site import get_website_settings
from bot.services.scraper.scraper import fetch_schedules
from bot.utils.schedule import format_schedule_text, get_user_group_data, get_current_week, week_days

router = Router()


@router.callback_query(F.data.in_([f"{day['name']}|{day['id']}" for day in week_days]))
@router.callback_query(F.message.text == "Виберіть групу ⬇️")
async def get_schedule(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Handles the displays the schedule."""
    week = get_current_week()
    website_settings = await get_website_settings(session=session)
    year = website_settings.year
    semester = website_settings.semester

    faculty, course, group, group_name, selected_day, selected_day_id = await get_user_group_data(
        session=session, call=call, state=state
    )

    subjects = await fetch_schedules(
        week=week, day=selected_day_id, faculty=faculty, course=course, group=group, year_id=year, semester=semester
    )

    text = format_schedule_text(subjects=subjects, week=week, selected_day=selected_day, group_name=group_name)
    await call.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN)
    await state.clear()
