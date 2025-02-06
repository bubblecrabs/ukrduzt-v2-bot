from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.start.inline import start_kb
from bot.utils.utils import get_current_week

router = Router()


def generate_start_text() -> str:
    """Generates the welcome text with the current week."""
    week = get_current_week()
    return (
        f"✋ Привіт, я допоможу дізнатися актуальний розклад на тиждень\n\n"
        f"📆 Поточна неділя - *{week}*"
    )


async def send_or_update_message(
        user_id: int, text: str, keyboard: InlineKeyboardMarkup, state: FSMContext, bot: Bot
) -> None:
    """Sends a new message or updates the last bot message."""
    previous_message_id = (await state.get_data()).get("last_bot_message_id")

    if previous_message_id:
        await bot.delete_message(chat_id=user_id, message_id=previous_message_id)

    sent_message = await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
    await state.update_data(last_bot_message_id=sent_message.message_id)


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext) -> None:
    """Handles the /start command."""
    await send_or_update_message(
        user_id=message.from_user.id,
        text=generate_start_text(),
        keyboard=await start_kb(message.from_user.id),
        state=state,
        bot=message.bot
    )


@router.callback_query(F.data == "start")
async def start_callback(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the start callback query."""
    await send_or_update_message(
        user_id=call.from_user.id,
        text=generate_start_text(),
        keyboard=await start_kb(call.from_user.id),
        state=state,
        bot=call.bot
    )
