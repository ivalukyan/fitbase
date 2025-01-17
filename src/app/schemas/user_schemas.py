from pydantic import BaseModel


class UserSchemas(BaseModel):
    id: int
    username: str
    phone: str
    telegram_id: int
    email: str | None = None
    msg: str | None = None
    
    class Config:
        orm_mode = True
        from_attributes=True