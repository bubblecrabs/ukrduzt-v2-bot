import csv
import os
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import AdminFilter
from bot.services.database.requests.users import get_users
from bot.utils.admin import get_username_bot

router = Router()


@router.callback_query(F.data == "export_users", AdminFilter())
async def export_users(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles for export all users to a CSV file."""
    users = await get_users(session=session)
    username_bot = await get_username_bot()

    file_path = f"users_{username_bot}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["User ID", "Username", "Faculty", "Course", "Group", "Group Name", "Is Admin", "Created At"])

            for user in users:
                writer.writerow([
                    user.user_id,
                    user.username or "N/A",
                    user.user_faculty or "N/A",
                    user.user_course or "N/A",
                    user.user_group or "N/A",
                    user.user_group_name or "N/A",
                    "Yes" if user.is_admin else "No",
                    user.created_at.strftime('%d.%m.%Y %H:%M')
                ])

        await call.message.delete()
        await call.message.answer_document(
            document=FSInputFile(file_path),
            caption=(
                f"📂 *Cписок користувачів:* `@{username_bot}`\n"
                f"🕒 *Дата отримання:* *{datetime.now().strftime('%d.%m.%Y %H:%M')}*"
            )
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
