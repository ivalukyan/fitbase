from fastapi import APIRouter, HTTPException, status
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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db_session: Session = Depends(get_db_session)) -> Token:
    admin = await authenticate_admin(db_session, form_data.username)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(data={"sub": form_data.username})

    return Token(access_token=access_token, token_type="bearer", expires_in=30)
