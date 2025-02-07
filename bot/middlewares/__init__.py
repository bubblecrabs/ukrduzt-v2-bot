from aiogram import Dispatcher


def register_middlewares(dp: Dispatcher) -> None:
    from .database import DatabaseMiddleware
    from .logging import LoggingMiddleware

    dp.update.outer_middleware(DatabaseMiddleware())
    dp.update.outer_middleware(LoggingMiddleware())
