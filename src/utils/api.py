import asyncio
import os
import sys

import httpx
import pandas as pd
import ujson

from asyncio import sleep
from os import getenv
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fitbase_api.api import FitbaseAPI
from src.utils.db import get_all_users


load_dotenv()

token = getenv("TOKEN")
domain = getenv("DOMAIN")

api = FitbaseAPI(fitbase_token=token, domain=domain)


def extract_contact(list_contacts):
    if not list_contacts:
        return None
    return list_contacts[0].get("contact", None)


async def update_database():

    headers = {
        "Club": domain,
        "Authorization": f"Bearer {token}"
    }

    query = {
        "page": 1,
    }

    url = f"https://api.fitbase.io/api/v2/client"
    async with httpx.AsyncClient() as c:
        response = await c.get(url=url, headers=headers, params=query)
    res = ujson.loads(response.text)
    if response.status_code == 200:
        total_count  = res['total_count']
        all_users = await get_all_users()

        if total_count > len(all_users):
            clients = await api.clients_all()

            df = pd.DataFrame(clients)

            df['contact'] = df['contacts'].apply(extract_contact)
            result = df[['name', 'surname', 'birth_date', 'contact']]
            print(result)
    else:
        print(response.text)



if __name__ == "__main__":
    asyncio.run(update_database())