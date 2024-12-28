from app.fitbase_api.api import FitbaseAPI
from dotenv import load_dotenv
from os import getenv

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