"""
Utils DB
"""
import logging
from database.models import SessionMaker
from database.models import User, Standards, Admin
from admin_app.schemas.user_schemas import UserSchemas

db = SessionMaker()


async def add_user(username: str, phone: str, telegram_id: int, email: str | None = None):
    user = User(username=username, phone=phone, email=email, telegram_id=telegram_id)
    db.add(user)
    db.commit()


async def update_user(telegram_id: int, username: str, phone: str, email: str):
    db.query(User).filter(User.telegram_id == telegram_id).update({'username': username, 'phone': phone,
                                                                   'email': email, 'telegram_id': telegram_id})
    db.commit()


async def get_user_by_telegram_id(telegram_id: int) -> bool:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        return False
    return True


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


async def add_standard(telegram_id: int):
    standard = Standards(telegram_id=telegram_id)
    db.add(standard)
    db.commit()


async def update_standard(telegram_id: int, grom: str, turkish_barbell_lifting: int, jump_rope: int, bench_press: int,
                          rod_length: int, shuttle_run: int, glute_bridge: int, pull_ups: int, cubic_jumps: int,
                          lifting_the_barbell_on_the_chest: int, axel_deadlift: int, handstand: str, classic_squat: int,
                          turkish_kettlebell_lifting: int, push_ups: int, lifting_barbell_on_the_chest: int,
                          walking_kettlebells: int, deadlift: int, long_jump: int, barbell_jerk: int, axel_hold: str,
                          front_squat: str):
    db.query(Standards).filter(Standards.telegram_id == telegram_id).update({'grom': grom,
                                                                             'turkish_barbell_lifting':turkish_barbell_lifting,
                                                                             'jump_rope': jump_rope,
                                                                             'bench_press': bench_press,
                                                                             'rod_length': rod_length,
                                                                             'shuttle_run': shuttle_run,
                                                                             'glute_bridge': glute_bridge,
                                                                             'pull_ups': pull_ups,
                                                                             'cubic_jumps': cubic_jumps,
                                                                             'lifting_the_barbell_on_the_chest': lifting_the_barbell_on_the_chest,
                                                                             'axel_deadlift': axel_deadlift,
                                                                             'handstand': handstand,
                                                                             'classic_squat': classic_squat,
                                                                             'turkish_kettlebell_lifting': turkish_kettlebell_lifting,
                                                                             'push_ups': push_ups,
                                                                             'lifting_barbell_on_the_chest': lifting_barbell_on_the_chest,
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
    return db.query(Standards).filter(Standards.telegram_id == telegram_id).first()


async def get_top_by_name(name: str):
    return db.query(getattr(Standards, name)).all()


async def get_admin_by_telegram_id(telegram_id: int):
    return db.query(Admin).filter(Admin.telegram_id == telegram_id).first()
