import asyncio
from uuid import uuid4

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove
)

from bot.handlers.menu import MESSAGES
from bot.handlers.menu import menu
from utils.bot import get_all_contacts, get_user_by_telegram_id
from utils.database import add_user, add_standard

router = Router()


@router.callback_query(F.data == "login")
async def login(call: CallbackQuery) -> None:

    if await get_user_by_telegram_id(call.message.chat.id):
        await menu(call)
        return
    await call.message.answer("Для авторизации отправьте свой номер телефона.",
                              reply_markup=ReplyKeyboardMarkup(keyboard=[
                                  [KeyboardButton(text="Поделится номером", request_contact=True)]
                              ],
                                  resize_keyboard=True,
                                  one_time_keyboard=True))
    MESSAGES.append(call.message.message_id)


@router.message(F.contact)
async def process_contact(message: Message) -> None:
    user_phone = message.contact.phone_number[-11:]

    contacts = await get_all_contacts()
    contacts.append('79687518203') # Удалить после тестирования

    if user_phone in contacts:
        await message.answer("Авторизация успешна! Добро пожаловать.", reply_markup=ReplyKeyboardRemove())
        MESSAGES.append(message.message_id)
        asyncio.create_task(add_user(username=message.from_user.first_name,
                                     phone=user_phone,
                                     telegram_id=message.from_user.id))
        asyncio.create_task(add_standard(telegram_id=message.from_user.id, username=message.from_user.first_name))
        callback_query = CallbackQuery(id=str(uuid4()), from_user=message.from_user, data="menu",
                                       message=message, chat_instance="auth")
        await menu(callback_query)
    else:
        await message.answer("Номер телефона не совпадает. Доступ запрещён.")
