from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.filters.admin import AdminFilter
from bot.keyboards.inline.admin import admin_kb, admin_func_kb
from bot.database.database import get_users_count, get_latest_user

router = Router()


@router.callback_query(F.data == "admin_menu", AdminFilter())
async def admin_menu(call: CallbackQuery) -> None:
    """Handler for the admin menu callback query."""
    await call.message.edit_text(
        text="Виберіть, що хочете зробити ⬇️",
        reply_markup=await admin_kb()
    )

@router.callback_query(F.data == "stats_bot", AdminFilter())
async def stats_bot(call: CallbackQuery) -> None:
    """Retrieves and displays the total number of users."""
    count = await get_users_count()
    latest_user = await get_latest_user()

    if latest_user:
        latest_user_info = (
            f"👤 *Останній зареєстрований:* `{latest_user.username or latest_user.user_id}`\n"
            f"🕒 *Час реєстрації:* {latest_user.created_at.strftime('%d.%m.%Y %H:%M')}"
        )
    else:
        latest_user_info = "\n*Користувачі не знайдені*"

    await call.message.edit_text(
        text=(
            f"📊 *Статистика*:\n\n"
            f"👥 *Кількість користувачів:* {count}\n"
            f"{latest_user_info}"
        ),
        reply_markup=await admin_func_kb()
    )
