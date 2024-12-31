from pydantic import BaseModel
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int | None = None


class AdminSchemas(BaseModel):
    id: UUID
    username: str
    phone: str
    password: str
    email: str | None = None
