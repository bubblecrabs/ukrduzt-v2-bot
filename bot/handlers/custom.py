from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.database.database import get_user_by_id
from bot.keyboards.inline.custom import course_kb, faculty_kb, group_kb, schedule_kb
from bot.services.scraper import fetch_faculties, fetch_schedules
from bot.services.utils.custom import format_schedule_text, get_user_group_data, week_days
from bot.services.utils.start import get_current_week
from bot.states.schedule import ScheduleState

router = Router()


@router.callback_query(F.data == "schedule")
async def get_day(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the schedule callback query."""
    user = await get_user_by_id(user_id=call.from_user.id)
    await call.message.edit_text(
        text="Виберіть день ⬇️",
        reply_markup=await schedule_kb(user.user_group),
    )
    await state.set_state(ScheduleState.day)


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


@router.callback_query(F.data.startswith("faculty_"))
async def get_course(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the selection of a faculty."""
    await state.update_data(faculty=call.data)
    await call.message.edit_text(
        text="Виберіть курс ⬇️",
        reply_markup=await course_kb(),
    )


@router.callback_query(F.data.startswith("course_"))
async def get_group(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the selection of a course."""
    await state.update_data(course=call.data)

    data = await state.get_data()
    faculty = data["faculty"].removeprefix("faculty_")
    course = data["course"].removeprefix("course_")

    await call.message.edit_text(
        text="Виберіть групу ⬇️",
        reply_markup=await group_kb(faculty, course),
    )


@router.callback_query(F.data.in_([f"{day['name']}|{day['id']}" for day in week_days]))
@router.callback_query(F.message.text == "Виберіть групу ⬇️")
async def get_schedule(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the selection of a group or day and displays the schedule."""
    week = get_current_week()
    faculty, course, group, group_name, selected_day, selected_day_id = await get_user_group_data(call, state)

    subjects = await fetch_schedules(week, selected_day_id, faculty, course, group)
    text = format_schedule_text(subjects, week, selected_day, group_name)

    await call.message.edit_text(text=text)
    await state.clear()
