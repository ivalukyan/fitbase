from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
)
from utils import get_standard_by_id

router = Router()


@router.callback_query(F.data == "normatives")
async def normative(call: CallbackQuery):
    text = ""
    standards = await get_standard_by_id(call.message.chat.id)
    if not standards:
        text = """
        <i>Данные о ваших нормативах отсутствуют.</i>
        """
    else:
        text = f"""
        <b>Данные по вашим нормативам.</b>
        
        - Гром: {standards.grom}
        - Турецкий подъем штанги: {standards.turkish_barbell_lifting}
        - Скакалка: {standards.jump_rope}
        - Жим лежа: {standards.bench_press}
        - Протяжка штанги: {standards.rod_length}
        - Челночный бег: {standards.shuttle_run}
        - Ягодичный мости: {standards.glute_bridge}
        - Подтягивания: {standards.pull_ups}
        - Прыжки на куб: {standards.cubic_jumps}
        - Взятие штанги на грудь (раз): {standards.lifting_barbell_on_the_chest_count}
        - Становая тяга акселя: {standards.axel_deadlift}
        - Стойка на руках: {standards.handstand}
        - Присед классический: {standards.classic_squat}
        - Турецкий подъем гири: {standards.turkish_kettlebell_lifting}
        - Отжимания от пола: {standards.push_ups}
        - Взятие штанги на грудь (кг): {standards.lifting_barbell_on_the_chest_kilo}
        - Прогулка с гирями: {standards.walking_kettlebells}
        - Становая тяга штанги: {standards.deadlift}
        - Прыжки в длину: {standards.long_jump}
        - Рывок штанги: {standards.barbell_jerk}
        - Удержание акселя: {standards.axel_hold}
        - Присед фронтальный: {standards.front_squat}
        """

    await call.message.edit_text(text=f"{text}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_menu")]
    ]))