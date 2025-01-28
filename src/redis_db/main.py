import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redis.asyncio import Redis

redis = Redis(host='redis', port=6379, db=0)