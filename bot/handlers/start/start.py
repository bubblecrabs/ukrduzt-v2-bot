from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.database.requests.site import set_year_and_semester
from bot.services.database.requests.users import add_user, get_user_is_admin
from bot.keyboards.inline.start import start_kb

router = Router()


@router.message(Command("start"))
@router.callback_query(F.data == "start")
async def start_command(event: Message | CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Handles the start command and callback query."""
    await state.clear()

    await set_year_and_semester(session=session)
    await add_user(session=session, user_id=event.from_user.id, username=event.from_user.username)
    is_admin = await get_user_is_admin(session=session, user_id=event.from_user.id)

    text_message = f"✋ Привіт, я допоможу дізнатися актуальний розклад на тиждень\\!"

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(
            text=text_message,
            reply_markup=await start_kb(is_admin=is_admin)
        )
    else:
        await event.answer(
            text=text_message,
            reply_markup=await start_kb(is_admin=is_admin)
        )
