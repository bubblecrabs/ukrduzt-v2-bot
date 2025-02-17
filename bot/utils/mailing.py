import asyncio
import logging
import re
from datetime import datetime, timezone

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.core.loader import bot, storage


def validate_url(text: str) -> bool:
    """Checks if the passed string is a valid URL of type HTTP/HTTPS or tg://."""
    http_pattern = r'^(https?:\/\/)([\da-z\.-]+)\.([a-z]{2,6})([\/\w \.-]*)*\/?$'
    tg_pattern = r'^tg:\/\/([a-zA-Z0-9_]+)$'
    if re.match(http_pattern, text, re.IGNORECASE):
        return True
    elif re.match(tg_pattern, text):
        return True
    else:
        return False


def decode_markdown_v2(text: str) -> str | None:
    """Decodes Markdown V2 formatted text by removing escape characters."""
    if text:
        pattern = r'\\([_*\[\]()~`>#+\-=|\\{}.!])'
        return re.sub(pattern, r'\1', text)
    return None


def generate_reply_markup(button_text: str, button_url: str) -> InlineKeyboardMarkup | None:
    """Generates an inline keyboard markup if a button is set."""
    if button_text and button_url:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=button_text, url=button_url)]])
    return None


def calculate_delay_seconds(delay: str) -> int | None:
    """Calculates the delay in seconds based on the provided timestamp."""
    if delay:
        scheduled_time = datetime.strptime(delay, "%d.%m.%Y %H:%M").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return max(0, int((scheduled_time - now).total_seconds()))
    return None


async def send_message(
        chat_id: int, text: str | None, image: str | None, reply_markup: InlineKeyboardMarkup | None
) -> None:
    """Sends a message to the user."""
    try:
        if image:
            await bot.send_photo(chat_id=chat_id, photo=image, caption=text, reply_markup=reply_markup)
        else:
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        await asyncio.sleep(1/30)
    except TelegramForbiddenError:
        logging.error(f"Failed to send message to {chat_id}. User blocked the bot.")
    except TelegramBadRequest as e:
        logging.error(f"Failed to send message to {chat_id}. {e}")


async def create_mailing_task(mailing_data: dict) -> None:
    """Pushes mailing data to Redis Stream."""
    converted_data = {k: v or "" for k, v in mailing_data.items()}
    await storage.redis.xadd("mailing_stream", converted_data)


async def process_message(entry_id: str, data: dict) -> None:
    """Processes and sends an individual message."""
    chat_id = data.get("chat_id")
    text = data.get("text")
    image = decode_markdown_v2(data.get("image"))
    button_text = decode_markdown_v2(data.get("button_text"))
    button_url = decode_markdown_v2(data.get("button_url"))
    delay = decode_markdown_v2(data.get("delay"))

    delay_seconds = calculate_delay_seconds(delay)
    if delay_seconds:
        await asyncio.sleep(delay_seconds)

    reply_markup = generate_reply_markup(button_text, button_url)
    await send_message(chat_id, text, image, reply_markup)
    await storage.redis.xdel("mailing_stream", entry_id)


async def process_mailing() -> None:
    """Processes messages from Redis Stream and sends them to users."""
    while True:
        messages = await storage.redis.xread({"mailing_stream": "0"}, block=5000)
        for stream, entries in messages:
            for entry_id, entry in entries:
                try:
                    data = {k.decode(): v.decode() for k, v in entry.items()}
                    await process_message(entry_id, data)
                except Exception as e:
                    logging.error(f"Error processing message: {e}")
