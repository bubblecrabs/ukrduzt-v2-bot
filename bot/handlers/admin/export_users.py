import csv
import io
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import AdminFilter
from bot.services.database.requests.users import get_users_count, get_users
from bot.utils.admin import get_username_bot

router = Router()


@router.callback_query(F.data == "export_users", AdminFilter())
async def export_users(call: CallbackQuery, session: AsyncSession) -> None:
    """Handles export of all users to a CSV file efficiently with a progress bar."""
    username_bot = await get_username_bot()

    total_users = await get_users_count(session)
    if total_users == 0:
        await call.message.answer(text="⚠️ *У базі даних немає користувачів для експорту.*")
        return

    file_buffer = io.StringIO()
    writer = csv.writer(file_buffer)
    writer.writerow([
        "User ID", "Username", "Faculty", "Course", "Group", "Group Name", "Is Admin", "Created At"
    ])

    progress_message = await call.message.edit_text(text="📤 *Експорт почався - 0%*")
    processed = 0
    last_progress = 0

    async for user in get_users(session):
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

        processed += 1
        progress = (processed / total_users) * 100

        if int(progress) - last_progress >= 5:
            last_progress = int(progress)
            progress_bar = "■" * (last_progress // 5) + "□" * (20 - last_progress // 5)
            await progress_message.edit_text(
                text=(
                    f"📤 *Експорт даних - {last_progress}%*\n\n"
                    f"[{progress_bar}]"
                )
            )

    file_buffer.seek(0)
    filename = f"users_{username_bot}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    await progress_message.edit_text(text="✅ *Експорт завершено! Відправлення файлу...*")

    await call.message.answer_document(
        document=BufferedInputFile(file_buffer.getvalue().encode("utf-8"), filename=filename),
        caption=(
            f"📂 *Список користувачів:* `@{username_bot}`\n"
            f"🕒 *Дата отримання:* *{datetime.now().strftime('%d.%m.%Y %H:%M')}*"
        )
    )
