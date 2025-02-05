import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redis_db.main import redis


async def get_count_month_users(mon: int, cnt: int) -> None:
    key = mon - 1
    value = await redis.get("list_users")
    print(value)
    if int(value[key]) < cnt:
        value[key] = cnt
        await redis.set("list_users", value)

    print(await redis.get("list_users"))
    return await redis.get("list_users")