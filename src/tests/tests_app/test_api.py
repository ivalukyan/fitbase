import json
import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from fastapi import Request, HTTPException


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.main import app
from app.routers.admin_router import login_admin
from app.schemas.admin_schemas import AdminSchemas
from app.main import custom_401_handler


# Фикстура для mock Request
@pytest.fixture
def mock_request(mocker):
    return mocker.Mock(spec=Request)


# Фикстура для mock db
@pytest.fixture
def mock_db(mocker):
    return mocker.Mock()


# Фикстура для mock templates
@pytest.fixture
def mock_templates(mocker):
    return mocker.patch('app.routers.admin_router.templates')


@pytest.fixture
def mock_errors_template(mocker):
    return mocker.patch('app.templates.errors')


# Фикстура для клиента FastAPI
@pytest.fixture
def client():
    return TestClient(app)


# Фикстура для симуляции токена авторизации
@pytest.fixture
def valid_token():
    return "test-jwt-token"


class TestLoginAdmin:

    # Тест для успешного возврата шаблона
    def test_login_admin_returns_template_response(self, mock_request, mock_db, mock_templates):
        mock_templates.TemplateResponse.return_value = MagicMock(status_code=200)

        response = login_admin(request=mock_request, db=mock_db)

        mock_templates.TemplateResponse.assert_called_once_with(
            "login.html", {"request": mock_request}
        )
        assert response.status_code == 200

    # Тест для обработки ошибки отсутствующего шаблона
    def test_login_admin_handles_missing_template(self, mock_request, mock_db, mock_templates):
        # Мокаем ошибку отсутствующего шаблона
        mock_templates.TemplateResponse.side_effect = FileNotFoundError("Template not found")

        # Проверяем, что FileNotFoundError возбуждается
        with pytest.raises(FileNotFoundError, match="Template not found"):
            login_admin(request=mock_request, db=mock_db)

        mock_templates.TemplateResponse.assert_called_once_with(
            "login.html", {"request": mock_request}
        )


@pytest.mark.asyncio
class TestHomeAdmin:
    async def test_home(self, client, valid_token):
        # Мокаем функции получения пользователей и администраторов
        mock_users = [{"id": 1, "username": "user1"}, {"id": 2, "username": "user2"}]
        mock_admins = [{"id": 1, "username": "admin"}]

        # Патчим get_all_users и get_all_admins, чтобы они возвращали замоканные данные
        with patch("app.routers.admin_router.get_all_users", return_value=mock_users), \
                patch("app.routers.admin_router.get_all_admins", return_value=mock_admins):
            # Заголовки с токеном для авторизации
            headers = {"Authorization": f"Bearer {valid_token}"}

            # Отправляем GET-запрос к /home через клиент с заголовками
            response = client.get("/api/admin/home", headers=headers)

            # Проверяем, что ответ успешный (статус 200)
            assert response.status_code == 200

            # Проверяем, что возвращаемые данные содержат пользователей и администраторов
            assert "users" in response.json()
            assert "admins" in response.json()

            # Проверяем, что данные пользователей и администраторов корректны
            users_data = response.json()["users"]
            admins_data = response.json()["admins"]

            assert len(users_data) == 2
            assert len(admins_data) == 1
            assert users_data[0]["username"] == "user1"
            assert admins_data[0]["username"] == "admin"
