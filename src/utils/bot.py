from fnmatch import translate
from os import getenv

from db.models import Admin, User
from db.models import SessionMaker
from dotenv import load_dotenv
from fitbase_api.api import FitbaseAPI

db = SessionMaker()

load_dotenv()
TOKEN = getenv('TOKEN')
DOMAIN = getenv('DOMAIN')


async def get_all_contacts() -> list:
    api = FitbaseAPI(fitbase_token=TOKEN, domain=DOMAIN)

    arr_contacts = []

    contacts = await api.contacts_all()
    for c in contacts['items']:
        if c['contact_type'] == 'phone':
            arr_contacts.append(c['contact'])

    return arr_contacts


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
