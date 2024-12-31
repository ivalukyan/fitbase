from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from uuid import UUID

from admin_app.auth.dependencies import get_current_admin, get_db_session
from admin_app.schemas.admin_schemas import AdminSchemas

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

templates = Jinja2Templates(directory="admin_app/templates")


@router.get("/login", description="Авторизация администратора")
async def login_admin(request: Request, db: Session = Depends(get_db_session)):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/home", description="Главная страница")
async def home(request: Request, db: Session = Depends(get_db_session)):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/me", response_model=AdminSchemas, description="Профиль администратора")
async def get_admin_me(admin: AdminSchemas = Depends(get_current_admin)):
    return admin


@router.get("/normative", description="Получение результатов пользователей")
async def all_results(db: Session = Depends(get_db_session)):
    return {"msg": "Получение результатов"}


@router.post("/normative", description="Добавление результат норматива пользователя")
async def create_result(db: Session = Depends(get_db_session)):
    return {"msg": "Добавление результата норматива пользователя"}


@router.put("/normative/{id}", description="Изменение норматива пользователя")
async def update_result(id: UUID, db: Session = Depends(get_db_session)):
    return {"msg": "Обновление результата норматива пользователя"}


@router.delete("/normative/{id}", description="Удаление результата норматива пользователя")
async def delete_result(id: UUID, db: Session = Depends(get_db_session)):
    return {"msg": "Удаление результата норматива пользователя"}
