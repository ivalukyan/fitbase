from dataclasses import dataclass
from pydantic import BaseModel
from uuid import UUID


@dataclass
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int | None = None


@dataclass
class AdminSchemas(BaseModel):
    id: UUID
    username: str
    phone: str
    password: str
    email: str | None = None
