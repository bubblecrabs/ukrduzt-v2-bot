import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.core.config import settings

logging.basicConfig(
    level=settings.logging.level,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        """Middleware for logging incoming messages and callbacks."""
        if isinstance(event, Message):
            logger.info(f"Received message: {event.text} from {event.from_user.id}")
        elif isinstance(event, CallbackQuery):
            logger.info(f"Received callback: {event.data} from {event.from_user.id}")

        return await handler(event, data)
