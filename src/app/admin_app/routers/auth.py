from fastapi import APIRouter, HTTPException, status, Response, Request
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from admin_app.auth.dependencies import get_db_session, authenticate_admin
from admin_app.schemas.auth_schemas import Token
from admin_app.auth.utils import create_access_token

router = APIRouter(
    tags=['Авторизация'],
    prefix="/auth"
)


@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db_session: Session = Depends(get_db_session)) -> Token:
    admin = await authenticate_admin(db_session, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(data={"sub": form_data.username})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return Token(access_token=access_token, token_type="bearer", expires_in=30)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'msg': 'Токен удален'}
