from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


async def start_kb(admin: bool) -> InlineKeyboardMarkup:
    """Generates the start menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Розклад занять", callback_data="schedule"))
    if admin:
        kb.add(InlineKeyboardButton(text="⚡️ Панель розробника", callback_data="admin_menu"))
    kb.adjust(1)
    return kb.as_markup()
