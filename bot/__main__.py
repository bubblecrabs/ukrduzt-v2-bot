import asyncio
import logging

from aiogram import Router

from bot.core.loader import bot, dp
from bot.core.config import settings

from bot.middlewares.database import DbSessionMiddleware
from bot.handlers.admin import panel, stats, mailing, manage_admins
from bot.handlers.admin.site import semester, year
from bot.handlers.schedule import day, faculty, course, group, schedule
from bot.handlers.start import start
from bot.utils.backup import schedule_backup


def get_routers() -> list[Router]:
    """Return a list of all routers used in the bot."""
    router_categories = {
        "admin_routers": [
            panel.router,
            stats.router,
            mailing.router,
            manage_admins.router,
        ],
        "admin_site_routers": [
            year.router,
            semester.router,
        ],
        "schedule_routers": [
            day.router,
            faculty.router,
            course.router,
            group.router,
            schedule.router,
        ],
        "start_routers": [
            start.router,
        ],
    }
    return [router for routers in router_categories.values() for router in routers]


async def on_startup() -> None:
    """Function to execute on bot startup."""
    await bot.delete_webhook(drop_pending_updates=True)
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
