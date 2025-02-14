import asyncio
import csv

from io import StringIO
from datetime import datetime, timedelta, UTC

from aiogram import Router
from aiogram.types import BufferedInputFile

from bot.core.loader import bot
from bot.services.database.session import session_maker
from bot.services.database.models.user import User
from bot.services.database.requests.users import get_users, get_admins

router = Router()

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
CHUNK_SIZE = 40 * 1024 * 1024  # 40 MB


def generate_filename(base: str, index: int, total_parts: int) -> str:
    """Generates a file name given the part number and total number of parts."""
    suffix = f"_part{index+1}" if total_parts > 1 else ""
    return f"{base}{suffix}.csv"


async def write_user_data(writer: csv.writer, user: User) -> None:
    """Write user data to the CSV writer."""
    writer.writerow([
        user.user_id,
        user.username or "N/A",
        user.user_faculty or "N/A",
        user.user_course or "N/A",
        user.user_group or "N/A",
        user.user_group_name or "N/A",
        user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        user.is_admin
    ])


async def create_file_buffer() -> tuple[StringIO, csv.writer]:
    """Create a new file buffer and CSV writer."""
    buffer = StringIO()
    writer = csv.writer(buffer, delimiter=";")
    writer.writerow([
        "User ID", "Username", "Faculty", "Course", "Group", "Group Name", "Created At", "Is Admin"
    ])
    return buffer, writer


async def send_file_to_admins(filename: str, file_data: bytes, username_bot: str) -> None:
    """Send the file to all admins."""
    async with session_maker() as session:
        async for admin in get_admins(session=session):
            await bot.send_document(
                chat_id=admin.user_id,
                document=BufferedInputFile(file_data, filename=filename),
                caption=(
                    f"📂 *Автоматичний бекап користувачів:* `@{username_bot}`\n"
                    f"🕒 *Дата отримання:* *{datetime.now().strftime('%d.%m.%Y %H:%M')}*"
                )
            )


async def get_username_bot() -> str:
    """Retrieve the bot's username."""
    bot_info = await bot.get_me()
    return bot_info.username


async def generate_backup() -> None:
    """Generates a user backup and sends it to admins, ensuring files do not exceed 50 MB."""
    username_bot = await get_username_bot()
    base_filename = f"users_{username_bot}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    file_buffers = []

    current_buffer, writer = await create_file_buffer()
    file_buffers.append(current_buffer)

    async with session_maker() as session:
        async for user in get_users(session=session):
            await write_user_data(writer, user)

            if current_buffer.tell() > CHUNK_SIZE:
                current_buffer, writer = await create_file_buffer()
                file_buffers.append(current_buffer)

    for index, buffer in enumerate(file_buffers):
        buffer.seek(0)
        filename = generate_filename(base_filename, index, len(file_buffers))
        file_data = buffer.getvalue().encode("utf-8")
        await send_file_to_admins(filename, file_data, username_bot)



async def schedule_backup() -> None:
    """Schedules the backup task to run every day at 03:00 UTC."""
    while True:
        now = datetime.now(UTC)
        next_run = datetime.combine(now.date(), datetime.min.time(), tzinfo=UTC) + timedelta(days=1, hours=3)
        if now.hour >= 3:
            next_run += timedelta(days=1)
        wait_time = (next_run - now).total_seconds()
        await asyncio.sleep(wait_time)
        await generate_backup()
