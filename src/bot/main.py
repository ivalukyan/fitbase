import asyncio
import logging
import sys
import os

from sqlalchemy.util import await_only

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from os import getenv
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, )
from dotenv import load_dotenv

from bot.handlers.menu import MESSAGES
from bot.handlers import admin
from bot.handlers.help import router as help_router
from bot.handlers.login import router as login_router
from bot.handlers.menu import router as menu_router
from bot.handlers.normatives import router as normatives_router
from bot.handlers.top import router as top_router

from redis.main import redis

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

router = Router()

bot_object = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                             InlineKeyboardButton(text="Войти", callback_data="login")
                         ]]))
    MESSAGES.append(message.message_id)

    exp = datetime(year=datetime.now().year, month=datetime.now().month + 1, day=1)
    await redis.hset("users", message.from_user.id,
                     f"user - {message.from_user.first_name}; username - {message.from_user.username}", expire=exp)


async def main():
    await redis.hset("stats_users", "one", 0)
    await redis.hset("stats_users", "two", 0)
    await redis.hset("stats_users", "three", 0)
    await redis.hset("stats_users", "four", 0)
    await redis.hset("stats_users", "five", 0)
    await redis.hset("stats_users", "six", 0)
    await redis.hset("stats_users", "seven", 0)
    await redis.hset("stats_users", "eight", 0)
    await redis.hset("stats_users", "nine", 0)
    await redis.hset("stats_users", "ten", 0)
    await redis.hset("stats_users", "eleven", 0)
    await redis.hset("stats_users", "twelve", 0)

    dp.include_routers(login_router, menu_router, normatives_router, top_router, admin.router, help_router, router)
    await dp.start_polling(bot_object)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
