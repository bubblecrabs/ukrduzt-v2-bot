from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.core.config import settings

bot = Bot(
    token=settings.bot.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
)

storage = RedisStorage.from_url(
    url=settings.redis.url
)

dp = Dispatcher(storage=storage)
