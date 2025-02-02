from datetime import datetime, timezone

import bcrypt
from app.schemas.admin_schemas import AdminSchemas
from database.models import SessionMaker, Admin
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status
from utils.security import SECRET_KEY, ALGORITHM


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


def check_password(stored_hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))


def get_db_session():
    session = SessionMaker()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        session.close()


async def get_admin(db_session: Session, phone: str):
    return db_session.query(Admin).filter(Admin.phone == phone).first()


async def authenticate_admin(db_session: Session, username: str, password: str):
    admin = await get_admin(db_session, username)
    if not admin:
        return None

    if not check_password(admin.password, password):
        return None
    return admin


async def get_current_admin(db_session: Session = Depends(get_db_session), token: str = Depends(get_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен не валидный",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    phone: str = payload.get("sub")
    if phone is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден номер пользователя')

    admin = await get_admin(db_session, phone)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    return AdminSchemas.from_orm(admin).dict()
