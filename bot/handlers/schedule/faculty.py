from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline.schedule import faculty_kb
from bot.services.scraper.scraper import fetch_faculties
from bot.utils.schedule import week_days

router = Router()


@router.callback_query(F.data.in_([f"{day['name']}_{day['id']}" for day in week_days]))
@router.callback_query(F.data.in_({"change_user_data", "poll_start"}))
async def get_faculty(call: CallbackQuery, state: FSMContext) -> None:
    """Handles callback queries for changing user data or selecting a day."""
    if call.data not in {"change_user_data", "poll_start"}:
        day_name, day_id = call.data.split("_")
        selected_day = next((day for day in week_days if day["id"] == day_id), week_days[0])
    else:
        selected_day = week_days[0]

    await state.update_data(day=f"{selected_day['name']}_{selected_day['id']}")

    faculties = await fetch_faculties()
    await call.message.edit_text(
        text="Виберіть факультатив ⬇️",
        reply_markup=await faculty_kb(faculties),
    )
