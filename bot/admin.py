from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, Message
)

router = Router()

@router.message(Command("admin"))
async def admin_endpoint(message: Message):
    text = f"""
    <b>АДМИН ПАНЕЛЬ</b>
    
    Здравствуйте, {message.from_user.first_name}
    """

    await message.answer(text=text, parse_mode="html", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сайт", url="https://ya.ru/")]
    ]))