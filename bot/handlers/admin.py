from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from bot.keyboards.inline import admin_kb
from bot.models.requests import db_count_users
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

@router.callback_query(F.data == "count_users", F.from_user.id == config.admin)
async def count_users(call: CallbackQuery) -> None:
    """Retrieves and displays the total number of users."""
    users_count: int = await db_count_users()
    await call.message.edit_text(
        text=f"👥 *Кількість користувачів:* {users_count}"
    )
