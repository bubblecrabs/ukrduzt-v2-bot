import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.config import Config
from bot.handlers import get_routers
from bot.database.setup import async_init_db
from bot.middlewares.logging import logger

config = Config()


async def main() -> None:
    """Initialize the database, set up the bot, and start polling."""

    # Initialize the database
    await async_init_db()

    # Create Bot instance with token and default properties
    bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )

    # Set up storage for FSM
    storage = RedisStorage.from_url(url=config.redis.url)

    # Set up Dispatcher
    dp = Dispatcher(storage=storage)

    # Include all the routers for handling commands and callbacks
    dp.include_routers(*get_routers())

    # Start polling for incoming updates
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
