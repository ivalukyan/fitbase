from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

router = Router()


@router.callback_query(F.data == "")
async def menu(call: CallbackQuery) -> None:
    await call.message.answer("Главное меню",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [InlineKeyboardButton(text="Нормативы", callback_data="normatives")],
                                  [InlineKeyboardButton(text="Топ", callback_data="top")]
                              ]))


@router.callback_query(F.data == "back_menu")
async def back_menu(call: CallbackQuery) -> None:
    await call.message.answer("Главное меню",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [InlineKeyboardButton(text="Нормативы", callback_data="normatives")],
                                  [InlineKeyboardButton(text="Топ", callback_data="top")]
                              ]))
