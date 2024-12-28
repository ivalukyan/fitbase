from dataclasses import dataclass
from pydantic import BaseModel
from uuid import UUID


@dataclass
class AdminSchemas(BaseModel):
    id: UUID
    username: str
    password: str
    phone: str
    email: str | None = None
