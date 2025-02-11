from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline.schedule import course_kb

router = Router()


@router.callback_query(F.data.startswith("faculty_"))
async def get_course(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the selection of a faculty."""
    await state.update_data(faculty=call.data)
    await call.message.edit_text(
        text="Виберіть курс ⬇️",
        reply_markup=await course_kb(),
    )
