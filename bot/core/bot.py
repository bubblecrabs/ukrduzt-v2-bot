from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.core.config import Config
from bot.core.logging import logging
from bot.handlers import get_routers
from bot.database.session import async_init_db

config = Config()


async def start_bot() -> None:
    """Initialize the database, set up the bot, and start polling."""
    logging.basicConfig(
        level=config.logging.level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    await async_init_db()

    bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )

    storage = RedisStorage.from_url(url=config.redis.url)

    dp = Dispatcher(storage=storage)
    dp.include_routers(*get_routers())

    await dp.start_polling(bot)
