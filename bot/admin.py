import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
)

from app.database.utils import get_top_by_name

router = Router()

@router.message(Command("admin"))
async def admin_endpoint(message: Message):
    text = f"""
    <b>АДМИН ПАНЕЛЬ</b>
    
    Здравствуйте, {message.from_user.first_name}
    """

    await message.answer(text=text, parse_mode="html", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сайт", url="http://localhost:8000")]
    ]))