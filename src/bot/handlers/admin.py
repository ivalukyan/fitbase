from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
)

from bot.main import bot_object
from utils.bot import get_admin_by_telegram_id, get_all_telegram_ids


router = Router()

class Form(StatesGroup):
    mailing = State()


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
            [InlineKeyboardButton(text="Сайт", url="http://87.249.53.163/api/admin/login")],
            [InlineKeyboardButton(text="Рассылка", callback_data="mailing")]
        ]))


@router.callback_query(F.data == "mailing")
async def callback_request_adm(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.mailing)
    await callback.message.edit_text("Введите сообщение для рассылки: ")


@router.message(Form.mailing)
async def request_adm(message: Message, state: FSMContext) -> None:
    mes = message.text
    users = await get_all_telegram_ids()
    for i in range(len(users)):
        await bot_object.send_message(int(users[i][0]), f"{mes}")

    await state.clear()