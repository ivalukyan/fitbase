import asyncio
import logging
import os
import sys
from os import getenv

import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fitbase_api.api import FitbaseAPI
from utils.database import get_all_users, add_user

# Load environment variables
load_dotenv()

token = getenv("TOKEN")
domain = getenv("DOMAIN")

if not token or not domain:
    raise ValueError("Environment variables TOKEN and DOMAIN must be set.")

api = FitbaseAPI(fitbase_token=token, domain=domain)


def extract_contact(list_contacts):
    """Extract the first contact from the list of contacts."""
    if not list_contacts:
        return None
    return list_contacts[0].get("contact")


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

    clients = await api.clients_all()

    if clients:
        logging.info(len(clients))
        all_users = await get_all_users()
        logging.info(len(all_users))

        if len(clients) > len(all_users):

            logging.info(type(clients))
            logging.info(type(all_users))

            df = pd.DataFrame(clients)
            df['contact'] = df['contacts'].apply(extract_contact)
            result = df[['name', 'surname', 'birth_date', 'contact']]

            await update_database(result)
        else:
            logging.info("No new clients to update.")
    else:
        logging.error(f"Error fetching clients.")


async def main():
    while True:
        logging.info("Fetching clients...")
        await fetch_clients()
        logging.info("Sleeping...")
        await asyncio.sleep(86400)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
