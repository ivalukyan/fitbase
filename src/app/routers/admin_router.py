import json
import logging
from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.util import await_only
from utils.database import (get_all_users, add_user, update_user, delete_user, get_all_admins, get_all_standards,
                   update_standard, add_standard, delete_standard, get_standard_by_id)

from app.auth.dependencies import get_current_admin, get_db_session
from app.schemas.admin_schemas import AdminSchemas, StatsUsersSchema
from app.schemas.normative_schemas import NormativeSchemas
from app.schemas.user_schemas import UserSchemas

from service.app_service import get_count_month_users
from utils.database import get_top_by_name

from redis_db.main import redis

router = APIRouter(
    prefix="/admin",
    tags=["Админ"],
)

templates = Jinja2Templates(directory="app/templates")


standards = {
    "Турецкий подъем штанги": "turkish_barbell_lifting",
    "Скакалка": "jump_rope",
    "Жим лежа": "bench_press",
    "Протяжка штанги": "rod_length",
    "Челночный бег": "shuttle_run",
    "Ягодичный мостик": "glute_bridge",
    "Подтягивания": "pull_ups",
    "Прыжки на куб": "cubic_jumps",
    "Взятие штанги на грудь (раз)": "lifting_barbell_on_the_chest_count",
    "Становая тяга акселя": "axel_deadlift",
    "Присед классический": "classic_squat",
    "Турецкий подъем гири": "turkish_kettlebell_lifting",
    "Отжимания от пола": "push_ups",
    "Взятие штанги на грудь (кг)": "lifting_barbell_on_the_chest_kilo",
    "Прогулка с гирями": "walking_kettlebells",
    "Становая тяга штанги": "deadlift",
    "Прыжки в длину": "long_jump",
    "Рывок штанги": "barbell_jerk",
    "Присед фронтальный": "front_squat",
}



@router.get("/login", description="Авторизация администратора")
async def login_admin(request: Request, db: Session = Depends(get_db_session)):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/home", description="Главная страница")
async def home(request: Request, admin: AdminSchemas = Depends(get_current_admin)):
    users = await get_all_users()
    admins = await get_all_admins()
    stats_normative = []

    for s in standards.values():
        sums = 0
        stats = await get_top_by_name(s)
        for t in range(len(stats)):
            sums += stats[t][0]
        stats_normative.append(sums / len(users))

    print(f"Статистика пользователей {stats_normative}")

    mon = datetime.now().month
    redis_users = await redis.hgetall("users")

    cnt = len({key.decode(): value.decode() for key, value in redis_users.items()})

    print(f"Количество пользователей {cnt}")

    stats_users = await get_count_month_users(mon, cnt)

    print(f"Статистика: {stats_users}")

    return templates.TemplateResponse("home.html", {"request": request,
                                                    "users": json.dumps(users),
                                                    "admins": json.dumps(admins),
                                                    "stats_users": stats_users,
                                                    "stats_normative": stats_normative})


@router.get("/me", response_model=AdminSchemas, description="Профиль администратора")
async def get_admin_me(admin: AdminSchemas = Depends(get_current_admin)):
    return admin


@router.get("/users", description="Получение всех пользователей")
async def get_admin_users(request: Request, admin: AdminSchemas = Depends(get_current_admin)):

    users = await get_all_users()

    return templates.TemplateResponse("users.html", {"request": request, 'users': json.dumps(users)})


@router.post("/users", description="Добавление пользователя", response_model=UserSchemas)
async def create_admin_user(user: UserSchemas, admin: AdminSchemas = Depends(get_current_admin)):
    await add_user(username=user.username, phone=user.phone, email=user.email, telegram_id=user.telegram_id)
    user.msg = 'Добавление пользователя'
    return user


@router.put("/users/{id}", description='Обновление данных пользователя', response_model=UserSchemas)
async def update_admin_user(id: int, user: UserSchemas, admin: AdminSchemas = Depends(get_current_admin)):
    await update_user(username=user.username, phone=user.phone, email=user.email, telegram_id=user.telegram_id)
    user.msg = 'Обновление пользователя'
    return user


@router.delete("/users/{id}", description='Удаление данных пользователя')
async def delete_admin_user(id: int, admin: AdminSchemas = Depends(get_current_admin)):
    await delete_user(telegram_id=id)
    return {'msg': 'Удаление данных пользователя'}


@router.get("/normative", description="Получение результатов пользователей")
async def all_results(request: Request, admin: AdminSchemas = Depends(get_current_admin)):
    normative = await get_all_standards()
    return templates.TemplateResponse("normative.html", {"request": request, 'normative': json.dumps(normative)})


@router.post("/normative", description="Добавление результат норматива пользователя", response_model=NormativeSchemas)
async def create_result(normative: NormativeSchemas, admin: AdminSchemas = Depends(get_current_admin)):
    await add_standard(username=normative.username, telegram_id=normative.telegram_id, grom=normative.grom,
                       turkish_barbell_lifting=normative.turkish_barbell_lifting, jump_rope=normative.jump_rope,
                       bench_press=normative.bench_press, rod_length=normative.rod_length, shuttle_run=normative.shuttle_run,
                       glute_bridge=normative.glute_bridge, pull_ups=normative.pull_ups, cubic_jumps=normative.cubic_jumps,
                       lifting_barbell_on_the_chest_count=normative.lifting_barbell_on_the_chest_count, axel_deadlift=normative.axel_deadlift,
                       handstand=normative.handstand, classic_squat=normative.classic_squat, turkish_kettlebell_lifting=normative.turkish_kettlebell_lifting,
                       push_ups=normative.push_ups, lifting_barbell_on_the_chest_kilo=normative.lifting_barbell_on_the_chest_kilo,
                       walking_kettlebells=normative.walking_kettlebells, deadlift=normative.deadlift, long_jump=normative.long_jump,
                       barbell_jerk=normative.barbell_jerk, axel_hold=normative.axel_hold, front_squat=normative.front_squat)
    normative.msg = f'Норматив для {normative.username} добавлен.'
    return normative


@router.get("/normative/{id}", description='Страница для обновления нормативов')
async def update_normative(request: Request, id: int, admin: AdminSchemas = Depends(get_current_admin)):
    normative = await get_standard_by_id(telegram_id=id)
    return templates.TemplateResponse('normative_update.html', {"request": request, 'normative': json.dumps(normative)})


@router.put("/normative/{id}", description="Изменение норматива пользователя", response_model=NormativeSchemas)
async def update_result(request: Request, id: int, normative: NormativeSchemas, admin: AdminSchemas = Depends(get_current_admin)):
    await update_standard(telegram_id=normative.telegram_id, grom=normative.grom,
                          turkish_barbell_lifting=normative.turkish_barbell_lifting, jump_rope=normative.jump_rope,
                          bench_press=normative.bench_press, rod_length=normative.rod_length,
                          shuttle_run=normative.shuttle_run, glute_bridge=normative.glute_bridge, pull_ups=normative.pull_ups,
                          cubic_jumps=normative.cubic_jumps, lifting_barbell_on_the_chest_count=normative.lifting_barbell_on_the_chest_count,
                          axel_deadlift=normative.axel_deadlift, handstand=normative.handstand, classic_squat=normative.classic_squat,
                          turkish_kettlebell_lifting=normative.turkish_kettlebell_lifting, push_ups=normative.push_ups,
                          lifting_barbell_on_the_chest_kilo=normative.lifting_barbell_on_the_chest_kilo,
                          walking_kettlebells=normative.walking_kettlebells, deadlift=normative.deadlift, long_jump=normative.long_jump,
                          barbell_jerk=normative.barbell_jerk, axel_hold=normative.axel_hold, front_squat=normative.front_squat)
    normative.msg = f"Обновление результатов нормативов {normative.username}."
    return normative


@router.delete("/normative/{id}", description="Удаление результата норматива пользователя")
async def delete_result(id: int, admin: AdminSchemas = Depends(get_current_admin)):
    await delete_standard(telegram_id=id)
    return {"msg": "Нормативы удалены"}
