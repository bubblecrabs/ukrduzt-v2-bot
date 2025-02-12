from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import AdminFilter
from bot.keyboards.inline.admin import admin_func_kb
from bot.services.database.requests.site import update_semester
from bot.states.site import SiteState

router = Router()


@router.callback_query(F.data == "update_semester", AdminFilter())
async def get_semester(call: CallbackQuery, state: FSMContext) -> None:
    """Handles semester update request."""
    await call.message.edit_text(
        text="✍️ *Введіть* `semester_id`*, який вказаний на сайті*",
        reply_markup=await admin_func_kb()
    )
    await state.set_state(SiteState.semester)


@router.message(StateFilter(SiteState.semester), AdminFilter())
async def set_semester(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Handles process semester update."""
    if message.text.isdigit() and message.text in {"1", "2"}:
            await update_semester(session=session, semester=int(message.text))
            await message.answer(text="✅ *Семестр успішно змінено*")
    else:
        await message.answer(
            text=(
                "❓ *Неправильний формат*\n\n"
                "❗️ *Семестр має бути, наприклад:* `1` або `2`"
            )
        )
    await state.clear()
