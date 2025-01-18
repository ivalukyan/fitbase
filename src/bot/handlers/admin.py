from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, Message
)
from utils.bot import get_admin_by_telegram_id


router = Router()

@router.message(Command("admin"))
async def admin_endpoint(message: Message):

    if not await get_admin_by_telegram_id(message.from_user.id):
        await message.answer(text="Данной команды не существует, попробуйте - /help")
    else:
        text = f"""
        <b>АДМИН ПАНЕЛЬ</b>
        
        Здравствуйте, {message.from_user.first_name}
        """

        await message.answer(text=text, parse_mode="html", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Сайт", url="http://127.0.0.1:8000/api/admin/login")]
        ]))