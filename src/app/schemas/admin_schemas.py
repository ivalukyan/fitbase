from pydantic import BaseModel


class AdminSchemas(BaseModel):
    id: int
    username: str
    password: str
    phone: str
    email: str | None = None

    class Config:
        orm_mode = True
        from_attributes=True
