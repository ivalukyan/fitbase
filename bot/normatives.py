from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
)

router = Router()


@router.callback_query(F.data == "normatives")
async def normative(call: CallbackQuery):
    await call.message.edit_text(text="Нормативы", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_menu")]
    ]))