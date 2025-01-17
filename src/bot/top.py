import logging

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
)

from src.utils.bot import get_top_by_name

router = Router()

# Список кнопок с текстом и уникальным callback_data, соответствующим полям модели
buttons = [
    ("Гром", "top_normative:grom"),
    ("Турецкий подъем штанги", "top_normative:turkish_barbell_lifting"),
    ("Скакалка", "top_normative:jump_rope"),
    ("Жим лежа", "top_normative:bench_press"),
    ("Протяжка штанги", "top_normative:rod_length"),
    ("Челночный бег", "top_normative:shuttle_run"),
    ("Ягодичный мостик", "top_normative:glute_bridge"),
    ("Подтягивания", "top_normative:pull_ups"),
    ("Прыжки на куб", "top_normative:cubic_jumps"),
    ("Взятие штанги на грудь (раз)", "top_normative:lifting_barbell_on_the_chest_count"),
    ("Становая тяга акселя", "top_normative:axel_deadlift"),
    ("Стойка на руках", "top_normative:handstand"),
    ("Присед классический", "top_normative:classic_squat"),
    ("Турецкий подъем гири", "top_normative:turkish_kettlebell_lifting"),
    ("Отжимания от пола", "top_normative:push_ups"),
    ("Взятие штанги на грудь (кг)", "top_normative:lifting_barbell_on_the_chest_kilo"),
    ("Прогулка с гирями", "top_normative:walking_kettlebells"),
    ("Становая тяга штанги", "top_normative:deadlift"),
    ("Прыжки в длину", "top_normative:long_jump"),
    ("Рывок штанги", "top_normative:barbell_jerk"),
    ("Удержание акселя", "top_normative:axel_hold"),
    ("Присед фронтальный", "top_normative:front_squat"),
    ("Назад", "back_menu")
]

# Разбиение кнопок на строки по 2 элемента
keyboard_rows = [
    [InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in buttons[i:i + 2]]
    for i in range(0, len(buttons), 2)
]


@router.callback_query(F.data == "top")
async def top(call: CallbackQuery):
    await call.message.edit_text(
        text="Нормативы.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    )


# Универсальный обработчик для всех кнопок
@router.callback_query(F.data.startswith("top_normative"))
async def handle_top_normative(call: CallbackQuery):

    action = call.data.split(":")[1]
    top = await get_top_by_name(action)

    if len(top) > 8:
        text = f"""
        <b>Результаты - Топ 10</b>
         - {top[0]}
         - {top[1]}
         - {top[2]}
         - {top[3]}
         - {top[4]}
         - {top[5]}
         - {top[6]}
         - {top[7]}
         - {top[8]}
         - {top[9]}
        """
    else:
        text = """
        <i>Для вывода статистики необходимы еще данные для статистики.</i>
        """

    await call.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад", callback_data="top")]
            ]
        )
    )
