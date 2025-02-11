from aiogram import Dispatcher


def register_middlewares(dp: Dispatcher) -> None:
    from .database import DbSessionMiddleware

    dp.update.outer_middleware(DbSessionMiddleware())
