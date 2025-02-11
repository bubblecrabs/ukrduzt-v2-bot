from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.filters.admin import AdminFilter
from bot.keyboards.inline.admin import admin_kb

router = Router()


@router.callback_query(F.data == "panel", AdminFilter())
async def admin_panel(call: CallbackQuery, state: FSMContext) -> None:
    """Handles for the admin menu callback query."""
    await state.clear()

    await call.message.edit_text(
        text="Виберіть, що хочете зробити ⬇️",
        reply_markup=await admin_kb()
    )
