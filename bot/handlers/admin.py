from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from bot.keyboards.inline import admin_kb, admin_func_kb
from bot.models.requests import get_users
from bot.config import config

router = Router()

@router.callback_query(F.data == "admin_menu", F.from_user.id == config.admin)
async def admin_menu(call: CallbackQuery) -> None:
    """Handler for the admin menu callback query."""
    keyboard: InlineKeyboardMarkup = await admin_kb()
    await call.message.edit_text(
        text="Виберіть, що хочете зробити ⬇️",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "stats_bot", F.from_user.id == config.admin)
async def stats_bot(call: CallbackQuery) -> None:
    """Retrieves and displays the total number of users."""
    keyboard: InlineKeyboardMarkup = await admin_func_kb()
    users = await get_users()

    sorted_users = sorted(users, key=lambda x: x.created_at, reverse=True)
    latest_user = sorted_users[0] if sorted_users else None

    latest_user_info = (
        f"👤 *Останній зареєстрований:* {latest_user.username or latest_user.user_id}\n"
        f"🕒 *Час реєстрації:* {latest_user.created_at.strftime('%d.%m.%Y %H:%M')}"
        if latest_user
        else "*Користувачі не знайдені*"
    )

    await call.message.edit_text(
        text=(
            f"📊 *Статистика*:\n\n"
            f"👥 *Кількість користувачів:* {len(users)}\n"
            f"{latest_user_info}"
        ),
        reply_markup=keyboard
    )
