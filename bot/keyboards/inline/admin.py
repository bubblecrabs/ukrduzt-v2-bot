from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


async def admin_kb() -> InlineKeyboardMarkup:
    """Generates the admin menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="👤 Статистика", callback_data="stats_bot"))
    kb.add(InlineKeyboardButton(text="📨 Повідомлення", callback_data="mailing"))
    kb.add(InlineKeyboardButton(text="🔑 Контроль доступу", callback_data="manage_admins"))
    kb.add(InlineKeyboardButton(text="📅 Оновити рік навчання", callback_data="update_year"))
    kb.add(InlineKeyboardButton(text="🎓 Оновити семестр", callback_data="update_semester"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="start"))
    kb.adjust(2, 1, 2, 1)
    return kb.as_markup()


async def admin_func_kb() -> InlineKeyboardMarkup:
    """Generates an administrator function menu keyboard."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="panel"))
    kb.adjust(1)
    return kb.as_markup()


async def confirm_mailing_kb() -> InlineKeyboardMarkup:
    """Generates a confirmation keyboard for mailing."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📨 Розпочати", callback_data="confirmed_mailing"))
    kb.add(InlineKeyboardButton(text="❌ Скасувати", callback_data="panel"))
    kb.adjust(2)
    return kb.as_markup()


async def manage_admins_kb() -> InlineKeyboardMarkup:
    """Generates a keyboard for administrators to manage."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="➕ Додати", callback_data="add_admin"))
    kb.add(InlineKeyboardButton(text="➖ Видалити", callback_data="delete_admin"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="panel"))
    kb.adjust(2, 1)
    return kb.as_markup()
