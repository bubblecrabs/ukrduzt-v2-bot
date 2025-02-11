from aiogram import Router

from .admin import admin, stats, export_users, mailing
from .custom import custom
from .start import start


def get_routers() -> list[Router]:
    """Return a list of all routers used in the bot."""
    return [
        start.router,
        custom.router,
        admin.router,
        stats.router,
        export_users.router,
        mailing.router,
    ]
