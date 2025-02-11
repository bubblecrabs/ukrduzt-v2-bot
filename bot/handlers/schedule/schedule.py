from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.scraper.scraper import fetch_schedules
from bot.utils.schedule import format_schedule_text, get_user_group_data, week_days
from bot.utils.start import get_current_week

router = Router()


@router.callback_query(F.data.in_([f"{day['name']}|{day['id']}" for day in week_days]))
@router.callback_query(F.message.text == "Виберіть групу ⬇️")
async def get_schedule(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Handles the selection of a group or day and displays the schedule."""
    week = get_current_week()
    faculty, course, group, group_name, selected_day, selected_day_id = await get_user_group_data(
        session=session,
        call=call,
        state=state
    )

    subjects = await fetch_schedules(week, selected_day_id, faculty, course, group)
    text = format_schedule_text(subjects, week, selected_day, group_name)

    await call.message.edit_text(text=text)
    await state.clear()
