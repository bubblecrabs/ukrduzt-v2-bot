from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class DatetimeFilter(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        """Custom filter to validate date format for messages and callbacks."""
        text = event.text if isinstance(event, Message) else event.message.text

        try:
            user_date = datetime.strptime(text, "%d.%m.%Y %H:%M")
            if user_date <= datetime.now():
                await event.answer(text="🚫 *Невірний формат, вказано минулий час*")
                return False
            return True

        except ValueError:
            await event.answer(text="🚫 *Невірний формат, спробуйте ще раз*")
            return False
