from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import start_kb
from bot.utils.utils import get_current_week

router = Router()

async def handle_start(
        user_id: int,
        edit_message: bool,
        message_obj: Message | CallbackQuery,
        state: FSMContext
) -> None:
    """Handles the start command logic, either by sending or editing a message."""
    week: str = get_current_week()
    text = (
        f"✋ Привіт, я допоможу дізнатися актуальний розклад на тиждень\n\n"
        f"📆 Поточна неділя - *{week}*"
    )
    keyboard: InlineKeyboardMarkup = await start_kb(user_id)

    # Check if the previous keyboard message should be deleted
    previous_message_id = (await state.get_data()).get("last_bot_message_id")
    if previous_message_id:
        try:
            await message_obj.bot.delete_message(chat_id=user_id, message_id=previous_message_id)
        except Exception:
            pass

    if edit_message:
        sent_message = await message_obj.message.edit_text(text=text, reply_markup=keyboard)
    else:
        sent_message = await message_obj.answer(text=text, reply_markup=keyboard)

    # Save the ID of the new message
    await state.update_data(last_bot_message_id=sent_message.message_id)


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext) -> None:
    """Handles the /start command to welcome the user and provide the current schedule."""
    await handle_start(
        user_id=message.from_user.id,
        edit_message=False,
        message_obj=message,
        state=state,
    )


@router.callback_query(F.data == "start")
async def start_callback(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the "start" callback query to provide the current schedule."""
    await handle_start(
        user_id=call.from_user.id,
        edit_message=True,
        message_obj=call,
        state=state,
    )
