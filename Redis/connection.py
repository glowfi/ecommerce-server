import os
from dotenv import find_dotenv, load_dotenv
import redis.asyncio as redis


# Load dotenv
load_dotenv(find_dotenv(".env"))


# RedisConnection
class RedisConnection:
    def __init__(self):
        self.DB_URL = os.getenv("DATABASE_URL")
        self.REDIS_URL = os.getenv("REDIS_URL")

    async def connect(self):
        pool = redis.ConnectionPool.from_url("redis://localhost")
        self.client = redis.Redis.from_pool(pool)
        print("Redis Connected!")

    async def disconnect(self):
        await self.client.close()
        print("Redis Disconnected!")


redis_connection = RedisConnection()
