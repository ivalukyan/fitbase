import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redis_db.main import redis


async def get_count_month_users(mon: int, cnt: int) -> None:
    month_mapping = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve"
    }

    if mon in month_mapping:
        key = month_mapping[mon]
        value = await redis.hget("stats_users", key)
        if value is None or int(value) < cnt:
            await redis.hset("stats_users", key, cnt)

    return await redis.hgetall("stats_users")