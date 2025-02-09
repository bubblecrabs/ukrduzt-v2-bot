from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from bot.services.scraper import fetch_groups
from bot.services.utils.custom import week_days


async def schedule_kb(user_group: int | None) -> InlineKeyboardMarkup:
    """Generates the schedule keyboard based on the user's group."""
    kb = InlineKeyboardBuilder()
    if user_group is not None:
        kb.add(InlineKeyboardButton(text="📝 Змінити групу", callback_data="change_user_data"))
    for day in week_days:
        callback_data = f"{day['name']}_{day['id']}" if user_group is None else f"{day['name']}|{day['id']}"
        kb.add(InlineKeyboardButton(text=day["name"], callback_data=callback_data))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="start"))
    kb.adjust(1)
    return kb.as_markup()


async def faculty_kb(faculties: dict[str, str]) -> InlineKeyboardMarkup:
    """Generates a keyboard for selecting faculties."""
    kb = InlineKeyboardBuilder()
    for faculty_id, faculty in faculties.items():
        kb.add(InlineKeyboardButton(text=faculty, callback_data=f"faculty_{faculty_id}"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="schedule"))
    kb.adjust(1)
    return kb.as_markup()


async def course_kb() -> InlineKeyboardMarkup:
    """Generates a keyboard for selecting a course."""
    kb = InlineKeyboardBuilder()
    for i in range(1, 7):
        kb.add(InlineKeyboardButton(text=f"{i}-й курс", callback_data=f"course_{i}"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="poll_start"))
    kb.adjust(1)
    return kb.as_markup()


async def group_kb(faculty: str, course: str) -> InlineKeyboardMarkup:
    """Generates a keyboard for selecting a group based on the user's faculty and course."""
    groups = await fetch_groups(faculty, course)
    kb = InlineKeyboardBuilder()
    for group_id, group_name in groups.items():
        kb.add(InlineKeyboardButton(text=group_name, callback_data=f"{group_id},{group_name}"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="poll_start"))
    kb.adjust(1)
    return kb.as_markup()
