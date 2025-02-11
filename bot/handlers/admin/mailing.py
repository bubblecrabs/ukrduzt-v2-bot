from datetime import datetime

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import AdminFilter
from bot.filters.datetime import DatetimeFilter
from bot.keyboards.inline.admin import admin_func_kb, confirm_mailing_kb
from bot.services.database.users import get_users_count
from bot.states.mailing import MailingState

router = Router()


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


@router.message(StateFilter(MailingState.time), AdminFilter(), DatetimeFilter())
async def confirm_mailing(message: Message, state: FSMContext) -> None:
    """Handles the validation of mailing time."""
    await state.update_data(time=message.text)
    data = await state.get_data()

    await message.answer(
        text=data["text"],
        reply_markup=await confirm_mailing_kb()
    )


@router.callback_query(F.data == "confirmed_mailing")
async def start_mailing(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    count_users = await get_users_count(session=session)

    await call.message.answer(
        text=f"✅ *Розсилку запущено для* `{count_users}` *користувачів*"
    )
