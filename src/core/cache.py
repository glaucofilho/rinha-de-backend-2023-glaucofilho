import redis.asyncio as redis

from core.configs import settings


class Cache:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=settings.REDIS_ADDRESS, port=settings.REDIS_PORT, db=0
        )

    async def set(self, key, value):
        client = redis.Redis(connection_pool=self.pool)
        await client.set(str(key), value)

    async def get(self, key):
        client = redis.Redis(connection_pool=self.pool)
        value = await client.get(str(key))
        return value if value else None
