from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
)

router = Router()
MESSAGES = []

@router.callback_query(F.data == "menu")
async def menu(call: CallbackQuery) -> None:
    await call.message.delete()
    await call.message.answer("<b>ГЛАВНОЕ МЕНЮ</b>",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                      [InlineKeyboardButton(text="Нормативы", callback_data="normatives")],
                                      [InlineKeyboardButton(text="Топ", callback_data="top")]
                                  ]))


@router.callback_query(F.data == "back_menu")
async def back_menu(call: CallbackQuery) -> None:
    await call.message.edit_text("<b>ГЛАВНОЕ МЕНЮ</b>",
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton(text="Нормативы", callback_data="normatives")],
                                     [InlineKeyboardButton(text="Топ", callback_data="top")]
                                 ]))
