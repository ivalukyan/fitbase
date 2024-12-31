from pydantic import BaseModel
from uuid import UUID


class AdminSchemas(BaseModel):
    id: UUID
    username: str
    password: str
    phone: str
    email: str | None = None
