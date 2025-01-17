from src.fitbase_api.api import FitbaseAPI
from dotenv import load_dotenv
from os import getenv
from src.database.models import SessionMaker
from src.database.models import Admin, User, Standards

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


async def add_user(username: str, phone: str, telegram_id: int, email: str | None = None):
    user = User(username=username, phone=phone, email=email, telegram_id=telegram_id)
    db.add(user)
    db.commit()


# Standard
async def add_standard(telegram_id: int, username: str):
    standard = Standards(telegram_id=telegram_id, username=username)
    db.add(standard)
    db.commit()

async def get_standard_by_id(telegram_id: int):
    return db.query(Standards).filter(Standards.telegram_id == telegram_id).first()


async def get_top_by_name(name: str):
    return db.query(getattr(Standards, name)).all()