from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards.custom.inline import schedule_kb, faculty_kb, course_kb, group_kb
from bot.fsm.states import Schedule
from bot.services.utils import get_current_week, week_days_first, week_days_h, is_weekend
from bot.services.scraper import fetch_faculties, fetch_schedules
from bot.database.requests import get_user_by_id, add_user, update_user

router = Router()


@router.callback_query(F.data == "schedule")
async def get_day(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the "schedule" callback query."""
    user = await add_user(user_id=call.from_user.id, username=call.from_user.username)
    await call.message.edit_text(
        text="Виберіть день ⬇️",
        reply_markup=await schedule_kb(user.user_group),
    )
    await state.set_state(Schedule.day)


@router.callback_query(F.data.in_({"change_user_data", "poll_start"}) | F.data.in_(week_days_first))
async def get_faculty(call: CallbackQuery, state: FSMContext) -> None:
    """Handles callback queries for changing user data or selecting a day."""
    await state.update_data(day=week_days_first[0] if call.data in {"change_user_data", "poll_start"} else call.data)
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
    groups = await state.get_data()
    await call.message.edit_text(
        text="Виберіть групу ⬇️",
        reply_markup=await group_kb(groups),
    )


async def get_user_group_data(state: FSMContext, call: CallbackQuery) -> tuple[str, str, str, str, str, str]:
    """Retrieves and processes user group data based on the callback query and FSM state."""
    user_data = await state.get_data()
    if call.message.text == "Виберіть групу ⬇️":
        group, group_name = call.data.split(",")
        faculty = user_data["faculty"].removeprefix("faculty_")
        course = user_data["course"].removeprefix("course_")
        selected_day, selected_day_id = user_data["day"].split("_")

        await update_user(
            faculty=int(faculty),
            course=int(course),
            group=int(group),
            group_name=group_name,
            user_id=call.from_user.id,
        )
    else:
        user = await get_user_by_id(call.from_user.id)
        faculty = user.user_faculty
        course = user.user_course
        group = user.user_group
        group_name = user.user_group_name
        selected_day, selected_day_id = call.data.split("|")

    return faculty, course, group, group_name, selected_day, selected_day_id


def format_schedule_text(subjects: dict[int, str], week: str, selected_day: str, group_name: str) -> str:
    """Formats the schedule text based on the provided data."""
    if subjects:
        week_str = "наступний" if is_weekend() else "цей"
        subjects_text = "\n".join(f"{sid}: *{sname}*" for sid, sname in subjects.items())
        return (
            f"🔔 Показано розклад на *{week_str}* тиждень\n\n"
            f"{subjects_text}\n\n"
            f"⏰ Вибраний день - *{selected_day}*\n"
            f"📆 Поточна неділя - *{week}*\n"
            f"💼 Вибрана група - *{group_name}*"
        )
    return (
            f"🔍 На *цей* день ваш розклад вільний\n\n"
            f"⏰ Вибраний день - *{selected_day}*\n"
            f"📆 Поточна неділя - *{week}*\n"
            f"💼 Вибрана група - *{group_name}*"
    )


@router.callback_query(F.data.in_(week_days_h))
@router.callback_query(F.message.text == "Виберіть групу ⬇️")
async def get_schedule(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the selection of a group or day and displays the schedule."""
    week = get_current_week()
    faculty, course, group, group_name, selected_day, selected_day_id = await get_user_group_data(state, call)

    subjects = await fetch_schedules(week, selected_day_id, faculty, course, group)
    text = format_schedule_text(subjects, week, selected_day, group_name)

    await call.message.edit_text(text=text)
    await state.clear()
