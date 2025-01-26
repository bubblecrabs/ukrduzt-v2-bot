from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import config


async def start_kb(user_id: int) -> InlineKeyboardMarkup:
    """Generates the start menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Розклад занять", callback_data="schedule"))
    if user_id == config.admin:
        kb.add(InlineKeyboardButton(text="⚡️ Панель розробника", callback_data="admin_menu"))
    kb.adjust(1)
    return kb.as_markup()
