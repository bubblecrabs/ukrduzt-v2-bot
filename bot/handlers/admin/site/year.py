from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import AdminFilter
from bot.keyboards.inline.admin import admin_func_kb
from bot.services.database.requests.site import update_year
from bot.states.site import SiteState

router = Router()


@router.callback_query(F.data == "update_year", AdminFilter())
async def get_year(call: CallbackQuery, state: FSMContext) -> None:
    """Handles year update request."""
    await call.message.edit_text(
        text="✍️ *Введіть* `year_id`*, який вказаний на сайті*",
        reply_markup=await admin_func_kb()
    )
    await state.set_state(SiteState.year)


@router.message(StateFilter(SiteState.year), AdminFilter())
async def set_year(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """Handles process year update."""
    if message.text.isdigit():
        await update_year(session=session, year=int(message.text))
        await message.answer(text="✅ *Рік навчання успішно змінено*")
        await state.clear()
    else:
        await message.answer(
            text=(
                "❓ *Неправильний формат*\n\n"
                "❗️ *Рік навчання має бути, наприклад:* `82`"
            )
        )
    await state.clear()
