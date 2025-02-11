from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


async def start_kb(is_admin: bool) -> InlineKeyboardMarkup:
    """Generates the start menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📆 Розклад занять", callback_data="schedule"))
    if is_admin:
        kb.add(InlineKeyboardButton(text="⚡️ Панель розробника", callback_data="panel"))
    kb.adjust(1)
    return kb.as_markup()
