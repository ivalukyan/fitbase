from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, Message
)
from app.database.utils import get_user_by_telegram_id

router = Router()


@router.message(Command("help"))
async def admin_endpoint(message: Message):

    if get_user_by_telegram_id(message.from_user.id):
        text = """
        <b>ДОСТУПНЫЕ КОМАНДЫ</b>
        
        <i>Данные бот предназначен для отслеживания текущих своих нормативов, а также статистики по этим нормативам.</i>
        
        - /start -- Начало использования бота.
        - /help -- Инструкция по использованию бота и доступные команды.
        """

        await message.answer(text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад в главное меню", callback_data="back_menu")]
        ]))
    else:
        text = """
        <b>ДОСТУПНЫЕ КОМАНДЫ</b>

        <i>Данные бот предназначен для отслеживания текущих своих нормативов, а также статистики по этим нормативам.</i>

        - /start -- Начало использования бота.
        - /help -- Инструкция по использованию бота и доступные команды.
        """

        await message.answer(text=text)