import redis
from redis.exceptions import ConnectionError

from core.configs import settings


class Cache:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=settings.REDIS_ADDRESS, port=settings.REDIS_PORT, db=0
        )
        self.redis_available = True

    async def set(self, key, value):
        if self.redis_available:
            try:
                client = redis.Redis(connection_pool=self.pool)
                await client.set(key, value)
            except ConnectionError:
                self.redis_available = False

    async def get(self, key):
        if self.redis_available:
            try:
                client = redis.Redis(connection_pool=self.pool)
                value = await client.get(key)
                return value.decode("utf-8") if value else None
            except ConnectionError:
                self.redis_available = False
        return None  # Return None if Redis is not available
