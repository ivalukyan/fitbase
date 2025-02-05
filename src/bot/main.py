import asyncio
import json
import logging
import sys
import os

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

from redis_db.main import redis

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

router = Router()

bot_object = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@router.message(CommandStart())
async def command_start(message: Message) -> None:

    if await redis.get("list_users") is None:
        await redis.set("list_users", json.dumps([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))

    logging.info(await redis.get("stats_users"))

    await message.answer(f"Здравствуйте, {message.from_user.first_name}!",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                             InlineKeyboardButton(text="Войти", callback_data="login")
                         ]]))
    MESSAGES.append(message.message_id)

    exp = datetime(year=datetime.now().year, month=datetime.now().month + 1, day=1)
    await redis.hset("users", message.from_user.id,
                     f"user - {message.from_user.first_name}; username - {message.from_user.username}")
    await redis.expireat("users", exp)


async def main():
    dp.include_routers(login_router, menu_router, normatives_router, top_router, admin.router, help_router, router)
    await dp.start_polling(bot_object)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
