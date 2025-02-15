from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


async def admin_kb() -> InlineKeyboardMarkup:
    """Generates the keyboard for the admin menu."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="👤 Статистика", callback_data="stats_bot"))
    kb.add(InlineKeyboardButton(text="📨 Повідомлення", callback_data="mailing_menu"))
    kb.add(InlineKeyboardButton(text="🔑 Контроль доступу", callback_data="manage_admins"))
    kb.add(InlineKeyboardButton(text="📅 Оновити рік навчання", callback_data="update_year"))
    kb.add(InlineKeyboardButton(text="🎓 Оновити семестр", callback_data="update_semester"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="start"))
    kb.adjust(2, 1, 2, 1)
    return kb.as_markup()


async def admin_func_kb() -> InlineKeyboardMarkup:
    """Generates the keyboard for administrator functions."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="panel"))
    kb.adjust(1)
    return kb.as_markup()


async def manage_admins_kb() -> InlineKeyboardMarkup:
    """Generates the keyboard for managing administrators."""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="➕ Додати", callback_data="add_admin"))
    kb.add(InlineKeyboardButton(text="➖ Видалити", callback_data="delete_admin"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="panel"))
    kb.adjust(2, 1)
    return kb.as_markup()


async def mailing_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📥 Почати розсилку", callback_data="start_mailing"))
    kb.add(InlineKeyboardButton(text="✍️ Текст", callback_data="add_text"))
    kb.add(InlineKeyboardButton(text="🖼 Медіа", callback_data="add_media"))
    kb.add(InlineKeyboardButton(text="⏹️ Кнопка", callback_data="add_button"))
    kb.add(InlineKeyboardButton(text="⏰ Запланувати", callback_data="add_delay"))
    kb.add(InlineKeyboardButton(text="🔄 Видалити інформацію", callback_data="reset_mailing"))
    kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="panel"))
    kb.adjust(1, 2, 2, 1)
    return kb.as_markup()

