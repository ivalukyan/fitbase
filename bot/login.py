from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
)

router = Router()


@router.callback_query(F.data == "login")
async def login(call: CallbackQuery) -> None:
    await call.message.answer("Для авторизации отправьте свой номер телефона.",
                              reply_markup=ReplyKeyboardMarkup(keyboard=[
                                  [KeyboardButton(text="Поделится номером", request_contact=True)]
                              ]))