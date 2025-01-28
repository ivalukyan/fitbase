import asyncio
import logging
import os
import sys
from datetime import datetime
from os import getenv

import httpx
import pandas as pd
import ujson
from dotenv import load_dotenv
from redis.asyncio import Redis

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fitbase_api.api import FitbaseAPI
from utils.database import get_all_users, add_user
from redis_db.main import redis


load_dotenv()

token = getenv("TOKEN")
domain = getenv("DOMAIN")
timeout = int(getenv("TIMEOUT"))

if not token or not domain:
    raise ValueError("Environment variables TOKEN and DOMAIN must be set.")

api = FitbaseAPI(fitbase_token=token, domain=domain)



def extract_contact(list_contacts):
    """Extract the first contact from the list of contacts."""
    if not list_contacts:
        return None
    return list_contacts[0].get("contact")


async def check_count_users_in_crm():
    headers = {
        "Club": domain,
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.fitbase.io/api/v2/client"
    async with httpx.AsyncClient() as c:
        response = await c.get(url=url, headers=headers)
    res = ujson.loads(response.text)
    return res['total_count']


async def update_database(clients_df):
    """Update the database with client information."""
    for _, client in clients_df.iterrows():
        user_data = {
            "username": client["name"] + " " + client["surname"],
            "phone": client["contact"]
        }
        logging.info(f"Updating user: {user_data}")
        await add_user(username=user_data["username"], phone=user_data["phone"])


async def fetch_clients():
    """Fetch client data from the Fitbase API and update the database if needed."""

    total = await redis.get('total_count')
    result = await check_count_users_in_crm()

    if total:

        if result > int(total):

            await redis.set('total_count', result)

            clients = await api.clients_all()
            all_users = await get_all_users()
            logging.info(f'Количество при запросе: {len(clients)}')
            logging.info(f'Количество из бд: {len(all_users)}')

            if len(all_users) > 0:
                slice_arr = len(all_users)
                cln = clients[slice_arr:]
                if len(cln) > 0:
                    df = pd.DataFrame(cln)
                    df['contact'] = df['contacts'].apply(extract_contact)
                    cln = df[['name', 'surname', 'birth_date', 'contact']]
                    logging.info(cln)
                    await update_database(cln)
                else:
                    logging.info(f"Not updated... total new: {len(cln)}")
            else:
                df = pd.DataFrame(clients)
                df['contact'] = df['contacts'].apply(extract_contact)
                result = df[['name', 'surname', 'birth_date', 'contact']]
                await update_database(result)
        else:
            logging.info("No new clients to update.")
    else:
        logging.error(f"Error fetching clients.")


async def main():
    await redis.set('total_count', 0)
    while True:
        logging.info("Fetching clients...")
        await fetch_clients()
        logging.info("Sleeping...")
        await asyncio.sleep(timeout)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
