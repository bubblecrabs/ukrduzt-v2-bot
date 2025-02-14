from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import AdminFilter
from bot.keyboards.inline.admin import manage_admins_kb, admin_func_kb
from bot.services.database.requests.users import update_admin
from bot.states.admin import AdminState

router = Router()


@router.callback_query(F.data == "manage_admins", AdminFilter())
async def manage_admins(call: CallbackQuery, state: FSMContext) -> None:
    """Handles for the manage_admins callback query."""
    await call.message.edit_text(
        text="Виберіть, що хочете зробити ⬇️",
        reply_markup=await manage_admins_kb()
    )
    await state.set_state(AdminState.func)


@router.callback_query(F.data.in_({"add_admin", "delete_admin"}), AdminFilter())
async def get_admin_id(call: CallbackQuery, state: FSMContext) -> None:
    """Handles for the add_admin and delete_admin callback query."""
    await state.update_data(func=call.data)
    await call.message.edit_text(
        text=(
            "✍️ *Введіть ID користувача або адміністратора*\n\n"
            "🔍 Отримати ID - `@getmyid_bot`"
        ),
        reply_markup=await admin_func_kb()
    )
    await state.set_state(AdminState.id)


@router.message(StateFilter(AdminState.id), AdminFilter())
async def set_admin(message: Message, state: FSMContext, session: AsyncSession):
    """Handles the change of admin status for user."""
    data = await state.get_data()

    if message.text.isdigit():
        user_id = int(message.text)
        admin = True if data["func"] == "add_admin" else False

        result = await update_admin(session=session, user_id=user_id, set_admin=admin)
        if not result:
            await message.answer(text=f"🚫 *Користувача не знайдено*")
        else:
            await message.answer(text=f"✅ *Статус користувача успішно змінено*")
    else:
        await message.answer(text="❓ *Неправильний ID користувача*")

    await state.clear()
