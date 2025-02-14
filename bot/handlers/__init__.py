import importlib
import pkgutil

from pathlib import Path
from aiogram import Router


def find_routers(package: str) -> list[Router]:
    """Recursively find all Router instances in the given package."""
    routers = []
    package_path = Path(package.replace(".", "/"))

    for _, module_name, _ in pkgutil.walk_packages([str(package_path)], prefix=f"{package}."):
        module = importlib.import_module(module_name)

        if hasattr(module, "router") and isinstance(getattr(module, "router"), Router):
            routers.append(getattr(module, "router"))

    return routers


def get_routers() -> list[Router]:
    """Find and return all routers in the bot.handlers package."""
    return find_routers("bot.handlers")
