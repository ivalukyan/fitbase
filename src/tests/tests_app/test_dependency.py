import os
import sys
import pytest
import bcrypt
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.auth.dependencies import get_token
from app.auth.dependencies import hash_password
from app.auth.dependencies import check_password
from app.auth.dependencies import get_db_session
from app.auth.dependencies import get_admin
from database.models import Admin

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


class TestCheckPassword:

    # Verify correct password matches stored hash
    def test_correct_password_matches_hash(self):
        # Arrange
        password = "123456"
        salt = bcrypt.gensalt()
        stored_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        stored_hash = stored_hash.decode('utf-8')


        # Act
        result = check_password(stored_hash, password)

        # Assert
        assert result is True

    # Handle empty password string
    def test_empty_password_returns_false(self):
        # Arrange
        password = ""
        salt = bcrypt.gensalt()
        stored_hash = bcrypt.hashpw("somepass".encode('utf-8'), salt).decode('utf-8')

        # Act
        result = check_password(stored_hash, password)

        # Assert
        assert result is False


class TestGetDbSession:

    # Session is successfully created and yielded
    def test_session_created_and_yielded(self, mocker):
        # Arrange
        mock_session = mocker.Mock()
        mock_session_maker = mocker.patch('app.auth.dependencies.SessionMaker', return_value=mock_session)

        # Act
        session_generator = get_db_session()
        session = next(session_generator)

        # Assert
        mock_session_maker.assert_called_once()
        assert session == mock_session
        try:
            next(session_generator)
        except StopIteration:
            mock_session.close.assert_called_once()


class TestGetAdmin:

    # Return admin object when phone number exists in database
    @pytest.mark.asyncio
    async def test_get_admin_returns_admin_when_phone_exists(self, mocker):
        # Arrange
        mock_db = mocker.Mock()
        mock_query = mocker.Mock()
        mock_filter = mocker.Mock()
        mock_admin = Admin(phone="1234567890", username="Test Admin")

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_admin

        # Act
        result = await get_admin(mock_db, "1234567890")

        # Assert
        assert result == mock_admin
        mock_db.query.assert_called_once_with(Admin)
        mock_query.filter.assert_called_once()

    # Handle empty string phone number
    @pytest.mark.asyncio
    async def test_get_admin_with_empty_phone(self, mocker):
        # Arrange
        mock_db = mocker.Mock()
        mock_query = mocker.Mock()
        mock_filter = mocker.Mock()

        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None

        # Act
        result = await get_admin(mock_db, "")

        # Assert
        assert result is None
        mock_db.query.assert_called_once_with(Admin)
        mock_query.filter.assert_called_once()