from pydantic import BaseModel
from typing import Dict


class AdminSchemas(BaseModel):
    id: int
    username: str
    password: str
    phone: str
    email: str | None = None

    class Config:
        from_attributes=True
        

class StatsUsersSchema(BaseModel):
    stats: list[int]
