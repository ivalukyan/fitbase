"""
Utils DB
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.schemas.admin_schemas import AdminSchemas
from app.schemas.normative_schemas import NormativeSchemas
from app.schemas.user_schemas import UserSchemas
from src.database.models import SessionMaker
from src.database.models import User, Standards, Admin

db = SessionMaker()


async def add_user(username: str, phone: str, email: str | None = None, telegram_id: int | None = None):
    user = User(username=username, phone=phone, email=email, telegram_id=telegram_id)
    db.add(user)
    db.commit()


async def update_user(telegram_id: int, username: str, phone: str, email: str):
    db.query(User).filter(User.telegram_id == telegram_id).update({'username': username, 'phone': phone,
                                                                   'email': email, 'telegram_id': telegram_id})
    db.commit()


async def get_all_users() -> list:
    users = db.query(User).all()

    data = []

    for user in users:
        data.append(UserSchemas.from_orm(user).dict())
    return data


async def delete_user(telegram_id: int):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    db.delete(user)
    db.commit()


async def get_all_standards() -> list:
    standards = db.query(Standards).all()

    data = []

    for standard in standards:
        data.append(NormativeSchemas.from_orm(standard).dict())
    return data


async def add_standard(telegram_id: int, username: str, grom: str, turkish_barbell_lifting: int,
                       jump_rope: int, bench_press: int, rod_length: int, shuttle_run: int, glute_bridge: int,
                       pull_ups: int,
                       cubic_jumps: int, lifting_barbell_on_the_chest_count: int, axel_deadlift: int, handstand: str,
                       classic_squat: int, turkish_kettlebell_lifting: int, push_ups: int,
                       lifting_barbell_on_the_chest_kilo: int,
                       walking_kettlebells: int, deadlift: int, long_jump: int, barbell_jerk: int, axel_hold: str,
                       front_squat: int):
    standard = Standards(telegram_id=telegram_id, username=username, grom=grom,
                         turkish_barbell_lifting=turkish_barbell_lifting,
                         jump_rope=jump_rope, bench_press=bench_press, rod_length=rod_length, shuttle_run=shuttle_run,
                         glute_bridge=glute_bridge, pull_ups=pull_ups, cubic_jumps=cubic_jumps,
                         lifting_barbell_on_the_chest_count=lifting_barbell_on_the_chest_count,
                         axel_deadlift=axel_deadlift,
                         handstand=handstand, classic_squat=classic_squat,
                         turkish_kettlebell_lifting=turkish_kettlebell_lifting,
                         push_ups=push_ups, lifting_barbell_on_the_chest_kilo=lifting_barbell_on_the_chest_kilo,
                         walking_kettlebells=walking_kettlebells, deadlift=deadlift, long_jump=long_jump,
                         barbell_jerk=barbell_jerk,
                         axel_hold=axel_hold, front_squat=front_squat)
    db.add(standard)
    db.commit()


async def update_standard(telegram_id: int, grom: str, turkish_barbell_lifting: int, jump_rope: int, bench_press: int,
                          rod_length: int, shuttle_run: int, glute_bridge: int, pull_ups: int, cubic_jumps: int,
                          lifting_barbell_on_the_chest_count: int, axel_deadlift: int, handstand: str,
                          classic_squat: int,
                          turkish_kettlebell_lifting: int, push_ups: int, lifting_barbell_on_the_chest_kilo: int,
                          walking_kettlebells: int, deadlift: int, long_jump: int, barbell_jerk: int, axel_hold: str,
                          front_squat: int):
    db.query(Standards).filter(Standards.telegram_id == telegram_id).update({'grom': grom,
                                                                             'turkish_barbell_lifting': turkish_barbell_lifting,
                                                                             'jump_rope': jump_rope,
                                                                             'bench_press': bench_press,
                                                                             'rod_length': rod_length,
                                                                             'shuttle_run': shuttle_run,
                                                                             'glute_bridge': glute_bridge,
                                                                             'pull_ups': pull_ups,
                                                                             'cubic_jumps': cubic_jumps,
                                                                             'lifting_barbell_on_the_chest_count': lifting_barbell_on_the_chest_count,
                                                                             'axel_deadlift': axel_deadlift,
                                                                             'handstand': handstand,
                                                                             'classic_squat': classic_squat,
                                                                             'turkish_kettlebell_lifting': turkish_kettlebell_lifting,
                                                                             'push_ups': push_ups,
                                                                             'lifting_barbell_on_the_chest_kilo': lifting_barbell_on_the_chest_kilo,
                                                                             'walking_kettlebells': walking_kettlebells,
                                                                             'deadlift': deadlift,
                                                                             'long_jump': long_jump,
                                                                             'barbell_jerk': barbell_jerk,
                                                                             'axel_hold': axel_hold,
                                                                             'front_squat': front_squat
                                                                             })
    db.commit()


async def delete_standard(telegram_id: int):
    db.query(Standards).filter(Standards.telegram_id == telegram_id).delete()
    db.commit()


async def get_standard_by_id(telegram_id: int):
    standard = db.query(Standards).filter(Standards.telegram_id == telegram_id).first()
    return NormativeSchemas.from_orm(standard).dict()


async def get_top_by_name(name: str):
    return db.query(getattr(Standards, name), Standards.username).all()


async def get_all_admins():
    admins = db.query(Admin).all()

    data = []

    for admin in admins:
        data.append(AdminSchemas.from_orm(admin).dict())
    return data
