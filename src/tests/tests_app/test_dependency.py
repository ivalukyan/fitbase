import os
import sys
import pytest
import bcrypt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.auth.dependencies import get_token
from app.auth.dependencies import hash_password

from fastapi import HTTPException
from starlette import status


class TestGetToken:

    # Return token when valid access token exists in cookies
    def test_get_token_returns_token_when_valid(self, mocker):
        # Arrange
        mock_request = mocker.Mock()
        mock_request.cookies = {'users_access_token': 'valid_token'}

        # Act
        result = get_token(request=mock_request)

        # Assert
        assert result == 'valid_token'

    # Raise 401 when no token exists in cookies
    def test_get_token_raises_401_when_missing(self, mocker):
        # Arrange
        mock_request = mocker.Mock()
        mock_request.cookies = {}

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_token(request=mock_request)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == 'Token not found'


class TestHashPassword:

    # Password is successfully hashed with bcrypt and returned as UTF-8 string
    def test_password_is_hashed_successfully(self):
        # Arrange
        password = "mypassword123"

        # Act
        hashed = hash_password(password)

        # Assert
        assert isinstance(hashed, str)
        assert bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    # Empty string password input
    def test_empty_password_is_hashed(self):
        # Arrange
        password = ""

        # Act
        hashed = hash_password(password)

        # Assert
        assert isinstance(hashed, str)
        assert bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
