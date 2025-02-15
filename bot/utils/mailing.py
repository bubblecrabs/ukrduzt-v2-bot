import asyncio
import logging

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from bot.core.loader import bot, storage

STREAM_NAME = "mailing_stream"


async def create_mailing_task(mailing_data: dict) -> None:
    """Pushes mailing data to Redis Stream."""
    converted_data = {
        k: "" if v is None else v for k, v in mailing_data.items()
    }
    await storage.redis.xadd(STREAM_NAME, converted_data)


async def process_mailing() -> None:
    """Processes messages from Redis Stream and sends them to users."""
    while True:
        try:
            messages = await storage.redis.xread({STREAM_NAME: "$"}, count=10, block=5000)
            for stream, entries in messages:
                for entry_id, entry in entries:
                    data = {k.decode(): v.decode() for k, v in entry.items()}
                    chat_id = data.get("chat_id")
                    text = data.get("text", "")
                    image = data.get("image")
                    button_text = data.get("button_text")
                    button_url = data.get("button_url")

                    reply_markup = None
                    if button_text and button_url:
                        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
                        reply_markup = InlineKeyboardMarkup(
                            inline_keyboard=[[InlineKeyboardButton(text=button_text, url=button_url)]]
                        )

                    try:
                        if image:
                            await bot.send_photo(
                                chat_id=chat_id,
                                photo=image,
                                caption=text,
                                reply_markup=reply_markup,
                                parse_mode=None
                            )
                        else:
                            await bot.send_message(
                                chat_id=chat_id,
                                text=text,
                                reply_markup=reply_markup,
                                parse_mode=None
                            )

                    except Exception as e:
                        logging.error(f"Failed to send message to {chat_id}. {e}")
                    except TelegramForbiddenError:
                        logging.error(f"Failed to send message to {chat_id}. User blocked the bot")

                    await storage.redis.xdel(STREAM_NAME, entry_id)
        except Exception as e:
            logging.error(f"Error processing mailing: {e}")
        await asyncio.sleep(1)
