from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.database.requests.users import get_latest_user, get_users_count
from bot.filters.admin import AdminFilter
from bot.keyboards.inline.admin import admin_func_kb

router = Router()


@router.callback_query(F.data == "stats_bot", AdminFilter())
async def stats_bot(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles for displays the total number of users."""
    count_users = await get_users_count(session=session)
    latest_user = await get_latest_user(session=session)

    username_or_id = latest_user.username if latest_user.username else latest_user.user_id
    registration_time = latest_user.created_at.strftime('%d\\.%m\\.%Y %H\\:%M')

    await call.message.edit_text(
        text=(
            f"📊 *Статистика*:\n\n"
            f"👥 *Кількість користувачів:* {count_users}\n"
            f"👤 *Останній зареєстрований:* `{username_or_id}`\n"
            f"🕒 *Час реєстрації:* {registration_time}"
        ),
        reply_markup=await admin_func_kb()
    )
