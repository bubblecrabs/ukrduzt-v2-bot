from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import config
from bot.utils.utils import week_days_first, week_days_h
from bot.utils.requests import get_groups


async def start_kb(user_id: int) -> InlineKeyboardMarkup:
    """Generates the start menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Розклад занять", callback_data="schedule"))
    if user_id == config.admin:
        kb.add(InlineKeyboardButton(text="⚡️ Панель розробника", callback_data="admin_menu"))
    kb.adjust(1)
    return kb.as_markup()


async def admin_kb() -> InlineKeyboardMarkup:
    """Generates the admin menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="👤 Статистика", callback_data="stats_bot"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="start"))
    kb.adjust(1)
    return kb.as_markup()


async def admin_func_kb() -> InlineKeyboardMarkup:
    """Generates an administrator function menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_menu"))
    kb.adjust(1)
    return kb.as_markup()


async def schedule_kb(user_group: str | None) -> InlineKeyboardMarkup:
    """Generates the schedule keyboard based on the user's group."""
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=week_day.split("_" if user_group is None else "|")[0],
            callback_data=week_day
        )
        for week_day in (week_days_first if user_group is None else week_days_h)
    ]
    if user_group is not None:
        kb.add(InlineKeyboardButton(text="📝 Змінити групу", callback_data="change_user_data"))
    kb.add(*buttons)
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="start"))
    kb.adjust(1)
    return kb.as_markup()


async def faculty_kb(faculties: dict[str, str]) -> InlineKeyboardMarkup:
    """Generates a keyboard for selecting faculties."""
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=faculty, callback_data=f'faculty_{faculty_id}')
        for faculty_id, faculty in faculties.items()
    ]
    kb.add(*buttons)
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="schedule"))
    kb.adjust(1)
    return kb.as_markup()


async def course_kb() -> InlineKeyboardMarkup:
    """Generates a keyboard for selecting a course."""
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=f'{i}-й курс', callback_data=f'course_{i}')
        for i in range(1, 7)  # Assuming courses are from 1 to 6
    ]
    kb.add(*buttons)
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="poll_start"))
    kb.adjust(1)
    return kb.as_markup()


async def group_kb(user_data: dict[str, str]) -> InlineKeyboardMarkup:
    """Generates a keyboard for selecting a group based on the user's faculty and course."""
    kb = InlineKeyboardBuilder()
    faculty = user_data["faculty"].split("_")[1]
    course = user_data["course"].split("_")[1]
    groups = await get_groups(faculty, course)
    buttons = [
        InlineKeyboardButton(text=group_name, callback_data=f"{group_id},{group_name}")
        for group_id, group_name in groups.items()
    ]
    kb.add(*buttons)
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="poll_start"))
    kb.adjust(1)
    return kb.as_markup()
