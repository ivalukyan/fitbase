"""
@Description: API для запросов к CRM Fitbase
"""
from asyncio import sleep
from typing import Any
from os import getenv

import pandas as pd
from dotenv import load_dotenv

import httpx
import ujson
import asyncio


load_dotenv()


class FitbaseAPI:
    def __init__(self, fitbase_token: str, domain: str) -> None:
        self.domain = domain
        self.headers = {
            "Club": domain,
            "Authorization": f"Bearer {fitbase_token}"
        }

    async def clients_all(self) -> str | Any:
        """
        @Description: Получение информации о всех клиентах
        :return:
        """
        data = []
        for i in range(1, 45):
            query = {
                "page": i,
                "page_size": 100,
            }
            url = f"https://api.fitbase.io/api/v2/client"
            async with httpx.AsyncClient() as c:
                response = await c.get(url=url, headers=self.headers, params=query)
            res = ujson.loads(response.text)
            if response.status_code == 200:
                data += res["items"]
        return data

    async def clients_by_id(self, client_id: int) -> str | Any:
        """
        @Description: Получение информации об отдельном клиенте
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/client/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка загрузки данных клиента. Попробуйте позже."
        return res

    async def create_client(self) -> str | Any:
        """
        @Description: Создание клиента
        :return:
        """
        url = "https://api.fitbase.io/api/v2/client"
        async with httpx.AsyncClient() as c:
            response = await c.post(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при добавлении клиента"
        return res

    async def delete_client(self, client_id: int) -> str | Any:
        """
        @Description: Удаление клиента
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/client/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.delete(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при удалении клиента"
        return res

    async def update_client(self, client_id: int) -> str | Any:
        """
        @Description: Обновление клиента
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/client/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.put(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при обновлении данных клиента"
        return res

    async def clients_contracts(self) -> str | Any:
        """
        @Description: Получение информации обо всех абонементах
        :return:
        """
        url = "https://api.fitbase.io/api/v2/client-contract"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка получения абонементов клиентов"
        return res

    async def client_contract(self, client_id: int) -> str | Any:
        """
        @Description: Информация об абонементе клиента
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/client-contract/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при получении информации об абонементе клиента"
        return res

    async def delete_client_contract(self, client_id: int) -> str | Any:
        """
        @Description: Удаление абонемента клинта
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/client-contract/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.delete(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка в удалении абонемента клиента"
        return res

    async def contacts_all(self):
        """
        @Description: Получение всех контактов клиентов
        :return:
        """
        url = "https://api.fitbase.io/api/v2/contact"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при получении контактов клиентов"
        return res

    async def contacts_by_id(self, client_id: int) -> str | Any:
        """
        @Description: Получение контакта конкретного клиента
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/contact/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при получении контакта клиента"
        return res

    async def delete_contact(self, client_id: int) -> str | Any:
        """
        @Description: Удаление контакта клиента
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/contact/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.delete(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при удалении контакта клиента"
        return res

    async def update_contact(self, client_id: int) -> str | Any:
        """
        @Description: Обновление контакта клиента
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/contact/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.put(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при обновлении контакта клиента"
        return res

    async def create_contact(self) -> str | Any:
        """
        @Description: Создание контакта клиента
        :return:
        """
        url = "https://api.fitbase.io/api/v2/contact"
        async with httpx.AsyncClient() as c:
            response = await c.post(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при создании нового контакта клиента"
        return res

    async def client_service_all(self) -> str | Any:
        """
        @Description: Получение всех услуг
        :return:
        """
        url = "https://api.fitbase.io/api/v2/client-service"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при загрузке услуг клиентов"
        return res

    async def client_service_by_id(self, client_id: int) -> str | Any:
        """
        @Description: Получение услуги клиента
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/client-service/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при получении услуги клиента"
        return res

    async def delete_client_service_by_id(self, client_id: int) -> str | Any:
        """
        @Description: Удаление услуги клиента
        :param client_id:
        :return:
        """
        url = f"https://api.fitbase.io/api/v2/client-service/{client_id}"
        async with httpx.AsyncClient() as c:
            response = await c.delete(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка при удалении услуги клиента"
        return res


def extract_contact(list_contacts):
    if not list_contacts:
        return None
    return list_contacts[0].get("contact", None)


async def main() -> None:
    token = getenv("TOKEN")
    domain = getenv("DOMAIN")

    api = FitbaseAPI(fitbase_token=token, domain=domain)

    # services = await api.client_service_all()
    # for service in services['items']:
    #     if service['service']['available_service']['archive'] is False:
    #         print(service['service']['available_service'])

    # contacts = await api.contacts_all()
    # for client in contacts['items']:
    #     if client['contact_type'] == 'phone':
    #         if client['contact'] == '79216281689':
    #             print(client['contact'])
    # Оформление таблицы с рамкой

    clients = await api.clients_all()

    df = pd.DataFrame(clients)

    df['contact'] = df['contacts'].apply(extract_contact)
    result = df[['name', 'surname', 'birth_date', 'card', 'contact']]

    print(result)


    # clients = await api.clients_all()
    # for client in clients['items']:
    #     print(client)


if __name__ == "__main__":
    asyncio.run(main())