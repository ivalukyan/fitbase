from datetime import datetime, timedelta, timezone
from os import getenv
from dotenv import load_dotenv

from jose import jwt
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = ("89288eaf33fdf7fb1c6645f16d8723d6e85c3c9123798f0a447681cd695045b9ff24da977d24414e49baacb0daa0144"
              "837c81bcea1baf6e3e362bbc0e0af3a8bda6b0690799c95124af43e31263b74d53ec422838afd35fecd5ee8402b5f67"
              "2bf2e2cf6429a1e0afdd46e64a1939412209793e2bb398df87269588e6cf790b42e00c247399529507183b4e6a7b714"
              "120e4febc0310a09d668f9227e67c73a4018bd6f6fa8a044dda678d9d3fdcab20eb5f09ea9390b7f5d1e1871054a8b1"
              "347db314297d4d300e06318f6f011b8177693ca09b5e0dbc6863d718409442d9d655da9e11b099c816e9bc08dd3e827"
              "2dd8cf7bc5993256c9445356f089fa42f6a34")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    UTC = timezone.utc

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt