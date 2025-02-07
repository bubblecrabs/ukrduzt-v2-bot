import asyncio

from bot.core.loader import bot, dp
from bot.handlers import get_routers
from bot.middlewares import register_middlewares


async def on_startup() -> None:
    """Function to execute on bot startup."""
    register_middlewares(dp)
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
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
