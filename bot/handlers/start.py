from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database.database import add_user, get_user_is_admin
from bot.keyboards.inline.start import start_kb
from bot.services.utils.start import generate_start_text

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext) -> None:
    """Handles the /start command."""
    await state.clear()

    await add_user(user_id=message.from_user.id, username=message.from_user.username)
    is_admin = await get_user_is_admin(user_id=message.from_user.id)

    await message.answer(
        text=generate_start_text(),
        reply_markup=await start_kb(is_admin=is_admin)
    )


@router.callback_query(F.data == "start")
async def start_callback(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the start callback query."""
    await state.clear()

    await add_user(user_id=call.from_user.id, username=call.from_user.username)
    is_admin = await get_user_is_admin(user_id=call.from_user.id)

    await call.message.edit_text(
        text=generate_start_text(),
        reply_markup=await start_kb(is_admin=is_admin)
    )
