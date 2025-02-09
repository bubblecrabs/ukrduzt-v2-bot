import csv
import os
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from bot.database.database import get_latest_user, get_users, get_users_count
from bot.filters.admin import AdminFilter
from bot.keyboards.inline.admin import admin_func_kb, admin_kb, confirm_mailing_kb
from bot.services.utils.admin import get_username_bot
from bot.states.mailing import MailingState

router = Router()


@router.callback_query(F.data == "admin_menu", AdminFilter())
async def admin_menu(call: CallbackQuery, state: FSMContext) -> None:
    """Handles for the admin menu callback query."""
    await state.clear()

    await call.message.edit_text(
        text="Виберіть, що хочете зробити ⬇️",
        reply_markup=await admin_kb()
    )


@router.callback_query(F.data == "stats_bot", AdminFilter())
async def stats_bot(call: CallbackQuery) -> None:
    """Handles for displays the total number of users."""
    count_users = await get_users_count()
    latest_user = await get_latest_user()

    await call.message.edit_text(
        text=(
            f"📊 *Статистика*:\n\n"
            f"👥 *Кількість користувачів:* {count_users}\n"
            f"👤 *Останній зареєстрований:* `{latest_user.username or latest_user.user_id}`\n"
            f"🕒 *Час реєстрації:* {latest_user.created_at.strftime('%d.%m.%Y %H:%M')}"
        ),
        reply_markup=await admin_func_kb()
    )


@router.callback_query(F.data == "export_users", AdminFilter())
async def export_users(call: CallbackQuery) -> None:
    """Handles for export all users to a CSV file."""
    users = await get_users()
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
                f"📂 *Cписок користувачів:* @{username_bot}\n"
                f"🕒 *Дата отримання:* *{datetime.now().strftime('%d.%m.%Y %H:%M')}*"
            )
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.callback_query(F.data == "mailing", AdminFilter())
async def mailing(call: CallbackQuery, state: FSMContext) -> None:
    """Handles for initiating a mailing process."""
    await call.message.edit_text(
        text="💬 *Введіть повідомлення для розсилки*",
        reply_markup=await admin_func_kb()
    )
    await state.set_state(MailingState.text)


@router.message(StateFilter(MailingState.text), AdminFilter())
async def set_time(message: Message, state: FSMContext) -> None:
    """Handles the text for the mailing time."""
    await state.update_data(text=message.text)
    await message.answer(
        text=(
            f"🕒 *Введіть дату і час розсилки*\n\n"
            f"📆 *Формат -* `{datetime.now().strftime('%d.%m.%Y %H:%M')}` *UTC+0*"
        ),
        reply_markup=await admin_func_kb()
    )
    await state.set_state(MailingState.time)


@router.message(StateFilter(MailingState.time), AdminFilter())
async def confirm_mailing(message: Message, state: FSMContext) -> None:
    """Handles the validation of mailing time."""
    try:
        user_date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        if user_date <= datetime.now():
            await message.answer(
                text="🚫 *Невірний формат, вказано минулий час*"
            )
        else:
            await state.update_data(time=message.text)
            data = await state.get_data()

            await message.answer(
                text=data["text"],
                reply_markup=await confirm_mailing_kb()
            )
    except ValueError:
        await message.answer(
            text="🚫 *Невірний формат, спробуйте ще раз*"
        )
