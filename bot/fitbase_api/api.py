"""
@Description: API для запросов к CRM Fitbase
"""
from typing import Any
from os import getenv
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
        url = "https://api.fitbase.io/api/v2/client"
        async with httpx.AsyncClient() as c:
            response = await c.get(url=url, headers=self.headers)
        res = ujson.loads(response.text)

        if not res:
            return "Ошибка загрузки данных"
        return res

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


async def main() -> None:

    token = getenv("TOKEN")
    domain = getenv("DOMAIN")

    api = FitbaseAPI(fitbase_token=token, domain=domain)

    contacts = await api.contacts_all()
    for client in contacts['items']:
        if client['contact_type'] == 'phone':
            print(client['contact'])


if __name__ == "__main__":
    asyncio.run(main())