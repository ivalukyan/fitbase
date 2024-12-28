from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from uuid import UUID

from bot.app.admin_app.auth.dependencies import get_current_admin, get_db_session
from bot.app.admin_app.schemas.admin_schemas import AdminSchemas

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/me", response_model=AdminSchemas)
async def get_admin_me(admin: AdminSchemas = Depends(get_current_admin)):
    return admin


@router.get("/normative")
async def all_results(db: Session = Depends(get_db_session)):
    return {"msg": "Получение результатов"}


@router.post("/normative")
async def create_result(db: Session = Depends(get_db_session)):
    return {"msg": "Добавление результата норматива пользователя"}


@router.put("/normative/{id}")
async def update_result(id: UUID, db: Session = Depends(get_db_session)):
    return {"msg": "Обновление результата норматива пользователя"}


@router.delete("/normative/{id}")
async def delete_result(id: UUID, db: Session = Depends(get_db_session)):
    return {"msg": "Удаление результата норматива пользователя"}
