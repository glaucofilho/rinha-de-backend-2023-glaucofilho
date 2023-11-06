import redis.asyncio as redis
from redis.exceptions import ConnectionError

from core.configs import settings


# def cache():
#     return redis.Redis(
#         host=settings.REDIS_ADDRESS,
#         port=settings.REDIS_PORT,
#     )


# class Cache:
#     def __init__(self):
#         self.pool = redis.ConnectionPool(
#             host=settings.REDIS_ADDRESS, port=settings.REDIS_PORT, db=0
#         )
#         self.redis_available = True

#     def set(self, key, value):
#         if self.redis_available:
#             try:
#                 client = redis.Redis(connection_pool=self.pool)
#                 client.set(key, value)
#             except ConnectionError:
#                 self.redis_available = False

#     def get(self, key):
#         if self.redis_available:
#             try:
#                 client = redis.Redis(connection_pool=self.pool)
#                 value = client.get(key)
#                 return value.decode("utf-8") if value else None
#             except ConnectionError:
#                 self.redis_available = False
#         return None


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
        return value.decode("utf-8") if value else None
