from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command

from bot.keyboards.inline import start_kb
from bot.utils.utils import get_current_week

router = Router()

async def handle_start(user_id: int, edit_message: bool, message_obj: Message | CallbackQuery) -> None:
    """Handles the start command logic, either by sending or editing a message."""
    week: str = get_current_week()
    text = (
        f"✋ Привіт, я допоможу дізнатися актуальний розклад на тиждень\n\n"
        f"📆 Поточна неділя - *{week}*"
    )
    keyboard: InlineKeyboardMarkup = await start_kb(user_id)

    if edit_message:
        await message_obj.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await message_obj.answer(text=text, reply_markup=keyboard)


@router.message(Command("start"))
async def start_command(message: Message) -> None:
    """Handles the /start command to welcome the user and provide the current schedule."""
    await handle_start(
        user_id=message.from_user.id,
        edit_message=False,
        message_obj=message,
    )


@router.callback_query(F.data == "start")
async def start_callback(call: CallbackQuery) -> None:
    """Handles the "start" callback query to provide the current schedule."""
    await handle_start(
        user_id=call.from_user.id,
        edit_message=True,
        message_obj=call,
    )
