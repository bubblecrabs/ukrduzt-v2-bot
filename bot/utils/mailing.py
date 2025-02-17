import re
import asyncio
from datetime import datetime, timezone

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from faststream import FastStream, Logger
from faststream.redis import RedisBroker

from bot.core.config import settings
from bot.core.loader import bot

broker = RedisBroker(url=settings.redis.url)
app = FastStream(broker)


def decode_markdown_v2(text: str | None) -> str:
    """Decodes Markdown V2 formatted text by removing escape characters."""
    return re.sub(r'\\([_*\[\]()~`>#+\-=|{}.!])', r'\1', text) if text else ""


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


async def send_message(
    chat_id: str, text: str, image: str | None, reply_markup: InlineKeyboardMarkup | None, logger: Logger
) -> None:
    """Sends a message to the user."""
    try:
        if image:
            await bot.send_photo(chat_id=chat_id, photo=image, caption=text, reply_markup=reply_markup)
        else:
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    except TelegramForbiddenError:
        logger.error(f"Failed to send message to {chat_id}. User blocked the bot.")
    except TelegramBadRequest as e:
        logger.error(f"Failed to send message to {chat_id}. {e}")


@broker.subscriber("mailing_stream")
async def process_message(data: dict, logger: Logger) -> None:
    """Processes and sends an individual message."""
    chat_id = data.get("chat_id")
    text = data.get("text")
    image = data.get("image")
    button_text = decode_markdown_v2(data.get("button_text"))
    button_url = decode_markdown_v2(data.get("button_url"))
    delay = decode_markdown_v2(data.get("delay"))

    if delay:
        delay_seconds = await calculate_delay_seconds(delay)
        if delay_seconds > 0:
            await asyncio.sleep(delay_seconds)

    reply_markup = generate_reply_markup(button_text, button_url)
    await send_message(chat_id, text, image, reply_markup, logger)


@app.after_startup
async def create_mailing_task(mailing_data: dict) -> None:
    """Pushes mailing data to Redis Stream."""
    await broker.publish(mailing_data, "mailing_stream")


async def process_mailing() -> None:
    await broker.start()
