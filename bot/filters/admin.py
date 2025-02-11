from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.database.users import get_user_is_admin


class AdminFilter(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery, session: AsyncSession) -> bool:
        """Custom filter to check if a user is an admin."""
        if not event.from_user:
            return False

        user_id = event.from_user.id
        return await get_user_is_admin(session=session, user_id=user_id)
