import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from os import getenv

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, )
from dotenv import load_dotenv

from bot.handlers.menu import MESSAGES
from bot.handlers.admin import router as admin_router
from bot.handlers.help import router as help_router
from bot.handlers.login import router as login_router
from bot.handlers.menu import router as menu_router
from bot.handlers.normatives import router as normatives_router
from bot.handlers.top import router as top_router

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

router = Router()


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                             InlineKeyboardButton(text="Войти", callback_data="login")
                         ]]))
    MESSAGES.append(message.message_id)


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(router, login_router, menu_router, normatives_router, top_router, admin_router, help_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
