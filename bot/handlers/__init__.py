from aiogram import Router

from . import start, admin, custom

def get_routers() -> list[Router]:
    """Return a list of all routers used in the bot."""
    return [
        start.router,
        admin.router,
        custom.router,
    ]
