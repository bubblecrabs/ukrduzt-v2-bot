import validators
from datetime import datetime

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import code
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.admin import AdminFilter
from bot.filters.datetime import DatetimeFilter
from bot.keyboards.inline.admin import admin_func_kb, mailing_menu_kb
from bot.services.database.requests.users import get_users
from bot.states.admin import MailingState
from bot.utils.mailing import create_mailing_task

router = Router()


@router.message(StateFilter(MailingState.menu))
@router.callback_query(F.data == "mailing_menu", AdminFilter())
async def mailing_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    """Handles displaying the mailing menu with current settings."""
    await state.set_state(MailingState.menu)
    message_data = await state.get_data()

    text = message_data.get("text", "Не встановлено")
    image = message_data.get("image", "Не встановлено")
    button_text = message_data.get("button_text", "Не встановлено")
    button_url = message_data.get("button_url", "Не встановлено")
    scheduled = message_data.get("delay", "Не заплановано")
    is_button_set = ("`Встановлено`" if button_text != "`Не встановлено`" else "`Не встановлено`")

    text_message = (
        f"ℹ️ *Інформація про розсилку:*\n\n"
        f"✍️ *Текст:* {code(text)}\n"
        f"🖼 *Зображення:* {code(image)}\n"
        f"⏹️ *Кнопка під текстом:* {is_button_set}\n"
        f"💬 *Текст кнопки:* {code(button_text)}\n"
        f"🔗 *Посилання кнопки:* {code(button_url)}\n"
        f"⏰ *Запланована розсилка:* {code(scheduled)}\n"
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(
            text=text_message,
            reply_markup=await mailing_menu_kb(),
            disable_web_page_preview=True
        )
    else:
        await event.answer(
            text=text_message,
            reply_markup=await mailing_menu_kb(),
            disable_web_page_preview=True
        )


@router.callback_query(F.data == "add_text", AdminFilter())
async def add_text(call: CallbackQuery, state: FSMContext) -> None:
    """Handles prompting the user to enter the text for the mailing."""
    await call.message.edit_text(
        text="💬 *Введіть повідомлення для розсилки\\.*",
        reply_markup=await admin_func_kb()
    )
    await state.set_state(MailingState.text)


@router.message(StateFilter(MailingState.text), AdminFilter())
async def set_text(message: Message, state: FSMContext) -> None:
    """Handles saving the entered text for the mailing and returning to the menu."""
    if len(message.text) > 3700:
        await message.answer(text="❌ *Максимальна довжина — 3700 символів\\. Спробуйте знову\\.*")
        return

    await state.update_data(text=message.text)
    await state.set_state(MailingState.menu)
    await mailing_menu(message, state)


@router.callback_query(F.data == "add_media", AdminFilter())
async def add_media(call: CallbackQuery, state: FSMContext) -> None:
    """Handles prompting the user to send an image for the mailing."""
    await call.message.edit_text(
        text="🖼 *Надішліть зображення для розсилки\\.*",
        reply_markup=await admin_func_kb()
    )
    await state.set_state(MailingState.media)


@router.message(StateFilter(MailingState.media), AdminFilter())
async def set_media(message: Message, state: FSMContext) -> None:
    """Handles saving the image for the mailing and returning to the menu."""
    if not message.photo:
        await message.answer("❌ *Надішліть будь ласка зображення\\.*")
        return

    photo_id = message.photo[-1].file_id
    await state.update_data(image=photo_id)
    await state.set_state(MailingState.menu)
    await mailing_menu(message, state)


@router.callback_query(F.data == "add_button", AdminFilter())
async def add_button(call: CallbackQuery, state: FSMContext) -> None:
    """Handles prompting the user to enter the button text for the mailing."""
    await call.message.edit_text(
        text="🔘 *Введіть текст кнопки\\.*",
        reply_markup=await admin_func_kb()
    )
    await state.set_state(MailingState.button_text)


@router.message(StateFilter(MailingState.button_text), AdminFilter())
async def set_button_text(message: Message, state: FSMContext) -> None:
    """Handles saving the button text and prompting the user to enter the button URL."""
    if len(message.text) > 35:
        await message.answer(text="❌ *Максимальна довжина — 35 символів\\. Спробуйте знову\\.*")
        return

    await state.update_data(button_text=message.text)
    await message.answer(text="🔗 *Введіть URL для кнопки\\.*")
    await state.set_state(MailingState.button_url)


@router.message(StateFilter(MailingState.button_url), AdminFilter())
async def set_button_url(message: Message, state: FSMContext) -> None:
    """Handles validating and saving the button URL, then returning to the menu."""
    if not validators.url(message.text):
        await message.answer(text="❌ *Невірний URL\\. Введіть коректне посилання\\.*")
        return

    await state.update_data(button_url=message.text)
    await state.set_state(MailingState.button_url)
    await mailing_menu(message, state)


@router.callback_query(F.data == "add_delay", AdminFilter())
async def add_delay(call: CallbackQuery, state: FSMContext) -> None:
    """Handles prompting the user to enter the delay for the scheduled mailing."""
    await call.message.edit_text(
        text=(
            f"🕒 *Введіть дату і час розсилки\\.*\n\n"
            f"📆 *Формат \\-* `{datetime.now().strftime('%d\\.%m\\.%Y %H\\:%M')}` *UTC\\+0*"
        ),
        reply_markup=await admin_func_kb()
    )
    await state.set_state(MailingState.delay)


@router.message(StateFilter(MailingState.delay), AdminFilter(), DatetimeFilter())
async def set_delay(message: Message, state: FSMContext) -> None:
    """Handles saving the scheduled delay for the mailing and returning to the menu."""
    await state.update_data(delay=message.text)
    await state.set_state(MailingState.menu)
    await mailing_menu(message, state)


@router.callback_query(F.data == "reset_mailing", AdminFilter())
async def reset_mailing(call: CallbackQuery, state: FSMContext) -> None:
    """Handles resetting all mailing settings and returning to the menu."""
    try:
        await state.clear()
        await state.set_state(MailingState.menu)
        await mailing_menu(call, state)
    except TelegramBadRequest:
        return


@router.callback_query(F.data == "start_mailing", AdminFilter())
async def start_mailing(call: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    """Handles starting the mailing process using the saved settings."""
    message_data = await state.get_data()

    text = message_data.get("text")
    image = message_data.get("image")
    button_text = message_data.get("button_text")
    button_url = message_data.get("button_url")
    delay = message_data.get("delay")

    if not text and not image:
        await call.message.answer(text="❌ *Ви не встановили текст або зображення для розсилки\\.*")
    else:
        await call.message.edit_text(text="✅ *Розсилку запущено\\.*")
        async for user in get_users(session):
            mailing_data = {
                "chat_id": str(user.user_id),
                "text": text,
                "image": image,
                "button_text": button_text,
                "button_url": button_url,
                "delay": delay
            }
            await create_mailing_task(mailing_data)
