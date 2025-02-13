from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.core.config import settings

bot = Bot(
    token=settings.bot.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)

storage = RedisStorage.from_url(
    url=settings.redis.url
)

dp = Dispatcher(storage=storage)
