import asyncio
import logging

from bot.core.loader import bot, dp
from bot.core.config import settings

from bot.middlewares.database import DbSessionMiddleware
from bot.handlers import get_routers
from bot.utils.backup import schedule_backup


async def on_startup() -> None:
    """Function to execute on bot startup."""
    dp.update.outer_middleware(DbSessionMiddleware())
    dp.include_routers(*get_routers())


async def on_shutdown() -> None:
    """Function to execute on bot shutdown."""
    await dp.storage.close()
    await dp.fsm.storage.close()
    await bot.session.close()


async def main() -> None:
    """Main function to start the bot."""
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await asyncio.gather(
        dp.start_polling(bot),
        schedule_backup()
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=settings.logging.level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    asyncio.run(main())
