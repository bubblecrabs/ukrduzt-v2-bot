import re
import asyncio
import logging
from datetime import datetime, timezone

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.core.loader import bot, storage

STREAM_NAME = "mailing_stream"


def decode_markdown_v2(text: str) -> str:
    """Decodes Markdown V2 formatted text by removing escape characters."""
    return re.sub(r'\\([_*[\]()~`>#+\-=|{}.!])', r'\1', text)


def generate_reply_markup(button_text: str, button_url: str) -> InlineKeyboardMarkup | None:
    """Generates an inline keyboard markup if a button is set."""
    if button_text and button_url:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=button_text, url=button_url)]])
    return None


async def calculate_delay_seconds(delay: str) -> int:
    """Calculates the delay in seconds based on the provided timestamp."""
    scheduled_time = datetime.strptime(delay, "%d.%m.%Y %H:%M").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    return max(0, int((scheduled_time - now).total_seconds()))


async def send_message(chat_id, text, image, reply_markup):
    """Sends a message to the user."""
    if image:
        await bot.send_photo(chat_id=chat_id, photo=image, caption=text, reply_markup=reply_markup)
    else:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


async def create_mailing_task(mailing_data: dict) -> None:
    """Pushes mailing data to Redis Stream."""
    converted_data = {k: "" if v is None else v for k, v in mailing_data.items()}
    await storage.redis.xadd(STREAM_NAME, converted_data)


async def fetch_mailing_messages() -> list:
    """Fetches messages from Redis Stream."""
    try:
        return await storage.redis.xread({STREAM_NAME: "0"}, count=10, block=5000)
    except Exception as e:
        logging.error(f"Error fetching messages: {e}")
        return []


async def process_message(entry_id, data):
    """Processes and sends an individual message."""
    chat_id = data.get("chat_id")
    text = data.get("text", "")
    image = data.get("image")
    button_text = decode_markdown_v2(data.get("button_text"))
    button_url = decode_markdown_v2(data.get("button_url"))
    delay = decode_markdown_v2(data.get("delay"))

    if delay:
        delay_seconds = await calculate_delay_seconds(delay)
        if delay_seconds > 0:
            await asyncio.sleep(delay_seconds)

    reply_markup = generate_reply_markup(button_text, button_url)

    try:
        await send_message(chat_id, text, image, reply_markup)
    except TelegramForbiddenError:
        logging.error(f"Failed to send message to {chat_id}. User blocked the bot.")
    except TelegramBadRequest as e:
        logging.error(f"Failed to send message to {chat_id}. {e}")
    finally:
        await storage.redis.xdel(STREAM_NAME, entry_id)


async def process_mailing() -> None:
    """Processes messages from Redis Stream and sends them to users."""
    while True:
        messages = await fetch_mailing_messages()
        for stream, entries in messages:
            for entry_id, entry in entries:
                try:
                    data = {k.decode(): v.decode() for k, v in entry.items()}
                    await process_message(entry_id, data)
                except Exception as e:
                    logging.error(f"Error processing message: {e}")
        await asyncio.sleep(1)
