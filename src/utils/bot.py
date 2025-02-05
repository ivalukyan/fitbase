from fnmatch import translate
from os import getenv

from database.models import Admin, User, Standards
from database.models import SessionMaker
from dotenv import load_dotenv
from fitbase_api.api import FitbaseAPI

db = SessionMaker()

load_dotenv()
TOKEN = getenv('TOKEN')
DOMAIN = getenv('DOMAIN')


async def get_all_telegram_ids():
    return db.query(User.telegram_id).all()


async def update_user_by_telegram(phone: str, telegram_id: int):
    db.query(User).filter(User.phone == phone).update({'telegram_id': telegram_id})
    db.commit()


async def add_standard_by_telegram(telegram_id: int, username: str):
    standard = Standards(telegram_id=telegram_id, username=username)
    db.add(standard)
    db.commit()


async def get_all_contacts():
    con =  db.query(User.phone).all()
    return [phone[0] for phone in con]

# Admin
async def get_admin_by_telegram_id(telegram_id: int):
    return db.query(Admin).filter(Admin.telegram_id == telegram_id).first()


# User
async def get_user_by_telegram_id(telegram_id: int) -> bool:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        return False
    return True


async def translate_top(standard) -> str:
    standards = {
        "grom": "Гром",
        "turkish_barbell_lifting": "Турецкий подъем штанги",
        "jump_rope": "Скакалка",
        "bench_press": "Жим лежа",
        "rod_length": "Протяжка штанги",
        "shuttle_run": "Челночный бег",
        "glute_bridge": "Ягодичный мостик",
        "pull_ups": "Подтягивания",
        "cubic_jumps": "Прыжки на куб",
        "lifting_barbell_on_the_chest_count": "Взятие штанги на грудь (раз)",
        "axel_deadlift": "Становая тяга акселя",
        "handstand": "Стойка на руках",
        "classic_squat": "Присед классический",
        "turkish_kettlebell_lifting": "Турецкий подъем гири",
        "push_ups": "Отжимания от пола",
        "lifting_barbell_on_the_chest_kilo": "Взятие штанги на грудь (кг)",
        "walking_kettlebells": "Прогулка с гирями",
        "deadlift": "Становая тяга штанги",
        "long_jump": "Прыжки в длину",
        "barbell_jerk": "Рывок штанги",
        "axel_hold": "Удержание акселя",
        "front_squat": "Присед фронтальный",
    }

    return standards[standard]
