import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import config
from bot.handlers import get_routers
from bot.database.models import async_init_db

# Set up logging for the bot
logging.basicConfig(level=config.logging_level)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Initialize the database, set up the bot, and start polling."""
    try:
        # Initialize the database asynchronously
        await async_init_db()
    except Exception as ex:
        logger.error(f"Database initialization failed: {ex}")
        return

    # Create Bot instance with token and default properties
    bot = Bot(
        token=config.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )

    # Set up storage for FSM
    storage = MemoryStorage()

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
