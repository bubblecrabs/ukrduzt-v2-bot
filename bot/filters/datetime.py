from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


class DatetimeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Custom filter to validate date format."""
        try:
            user_date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
            if user_date <= datetime.now():
                await message.answer(text="❌ *Невірний формат, вказано минулий час\\.*")
                return False
            return True
        except ValueError:
            await message.answer(text="❌ *Невірний формат, спробуйте знову\\.*")
            return False
