import asyncio
from uuid import uuid4
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, Message
)

from menu import menu
from utils import get_all_contacts

router = Router()


@router.callback_query(F.data == "login")
async def login(call: CallbackQuery) -> None:
    await call.message.answer("Для авторизации отправьте свой номер телефона.",
                              reply_markup=ReplyKeyboardMarkup(keyboard=[
                                  [KeyboardButton(text="Поделится номером", request_contact=True)]
                              ],
                                  resize_keyboard=True,
                                  one_time_keyboard=True))


@router.message(F.contact)
async def process_contact(message: Message) -> None:
    user_phone = message.contact.phone_number

    contacts = await get_all_contacts()

    if user_phone in contacts:
        await message.answer("Авторизация успешна! Добро пожаловать.")
        callback_query = CallbackQuery(id=str(uuid4()), from_user=message.from_user, data="menu",
                                       message=message, chat_instance="auth")
        await menu(callback_query)
    else:
        await message.answer("Номер телефона не совпадает. Доступ запрещён.")
