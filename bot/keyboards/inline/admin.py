from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


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
