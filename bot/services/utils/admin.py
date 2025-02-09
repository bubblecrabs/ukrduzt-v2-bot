from bot.core.loader import bot


async def get_username_bot() -> str:
    """Retrieve the bot's username."""
    bot_info = await bot.get_me()
    return bot_info.username
