import json
import os
import sys
import pytest

from fastapi import Request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.routers.admin_router import login_admin
from app.routers.admin_router import home
from app.schemas.admin_schemas import AdminSchemas


class TestLoginAdmin:

    # Returns 200 status code with login.html template
    @pytest.mark.asyncio
    async def test_login_admin_returns_template_response(self, mocker):
        mock_request = mocker.Mock()
        mock_db = mocker.Mock()
        mock_templates = mocker.patch('app.routers.admin_router.templates')
        mock_templates.TemplateResponse.return_value = mocker.Mock(status_code=200)

        response = await login_admin(request=mock_request, db=mock_db)

        mock_templates.TemplateResponse.assert_called_once_with(
            "login.html",
            {"request": mock_request}
        )
        assert response.status_code == 200

    # Handle missing template file
    @pytest.mark.asyncio
    async def test_login_admin_handles_missing_template(self, mocker):
        mock_request = mocker.Mock()
        mock_db = mocker.Mock()
        mock_templates = mocker.patch('app.routers.admin_router.templates')
        mock_templates.TemplateResponse.side_effect = FileNotFoundError("Template not found")

        with pytest.raises(FileNotFoundError):
            await login_admin(request=mock_request, db=mock_db)

        mock_templates.TemplateResponse.assert_called_once_with(
            "login.html",
            {"request": mock_request}
        )