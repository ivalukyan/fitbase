import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redis_db.main import redis


async def get_count_month_users(mon: int, cnt: int) -> list:
    key = mon - 1

    value_bytes = await redis.get("list_users")
    value_str = value_bytes.decode('utf-8')
    value = json.loads(value_str)

    if value[key] < cnt:
        value[key] = cnt
        await redis.set("list_users", json.dumps(value))

    updated_value_bytes = await redis.get("list_users")
    updated_value_str = updated_value_bytes.decode('utf-8')
    updated_value = json.loads(updated_value_str)

    return updated_value