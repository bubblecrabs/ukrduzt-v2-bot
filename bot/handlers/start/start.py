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
async def start_command(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Handles the /start command."""
    await state.clear()

    await set_year_and_semester(session=session)
    await add_user(session=session, user_id=message.from_user.id, username=message.from_user.username)
    is_admin = await get_user_is_admin(session=session, user_id=message.from_user.id)

    await message.answer(
        text=f"✋ Привіт, я допоможу дізнатися актуальний розклад на тиждень",
        reply_markup=await start_kb(is_admin=is_admin)
    )


@router.callback_query(F.data == "start")
async def start_callback(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Handles the start callback query."""
    await state.clear()

    await set_year_and_semester(session=session)
    await add_user(session=session, user_id=call.from_user.id, username=call.from_user.username)
    is_admin = await get_user_is_admin(session=session, user_id=call.from_user.id)

    await call.message.edit_text(
        text=f"✋ Привіт, я допоможу дізнатися актуальний розклад на тиждень",
        reply_markup=await start_kb(is_admin=is_admin)
    )
