from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline.schedule import group_kb

router = Router()


@router.callback_query(F.data.startswith("course_"))
async def get_group(call: CallbackQuery, state: FSMContext) -> None:
    """Handles the selection of a course."""
    await state.update_data(course=call.data)

    data = await state.get_data()
    faculty = data["faculty"].removeprefix("faculty_")
    course = data["course"].removeprefix("course_")

    await call.message.edit_text(
        text="Виберіть групу ⬇️",
        reply_markup=await group_kb(faculty, course),
    )
