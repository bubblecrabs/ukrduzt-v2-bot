from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline.schedule import schedule_kb
from bot.services.database.users import get_user_by_id
from bot.states.schedule import ScheduleState

router = Router()


@router.callback_query(F.data == "schedule")
async def get_day(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Handles the schedule callback query."""
    user = await get_user_by_id(session=session, user_id=call.from_user.id)
    await call.message.edit_text(
        text="Виберіть день ⬇️",
        reply_markup=await schedule_kb(user.user_group),
    )
    await state.set_state(ScheduleState.day)
