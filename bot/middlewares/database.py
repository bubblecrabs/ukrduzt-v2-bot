from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.services.database.session import session_maker


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Middleware for managing a database session."""
        async with session_maker() as session:
            data["session"] = session
            return await handler(event, data)
