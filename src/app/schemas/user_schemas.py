from pydantic import BaseModel


class UserSchemas(BaseModel):
    id: int
    username: str
    phone: str
    telegram_id: int | None = None
    email: str | None = None
    msg: str | None = None
    
    class Config:
        from_attributes=True