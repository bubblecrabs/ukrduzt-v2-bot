from aiogram import Router
from collections.abc import Sequence

from . import start, admin, custom

def get_routers() -> Sequence[Router]:
    """Return a list of all routers used in the bot."""
    return [
        start.router,
        admin.router,
        custom.router,
    ]
