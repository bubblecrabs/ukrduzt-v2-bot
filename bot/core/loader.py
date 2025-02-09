from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.core.config import settings
from bot.services.redis.cache import RedisCache


bot = Bot(
    token=settings.bot.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)

redis_cache = RedisCache(
    redis_url=settings.redis.url,
    ttl=settings.redis.ttl
)

storage = RedisStorage.from_url(
    url=settings.redis.url
)

dp = Dispatcher(storage=storage)
