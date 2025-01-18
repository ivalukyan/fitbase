from os import getenv

from database.models import Admin, User
from database.models import SessionMaker
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
