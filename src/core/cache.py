import pickle

import redis.asyncio as redis

from core.configs import settings


class Cache:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=settings.REDIS_ADDRESS, port=settings.REDIS_PORT, db=0
        )

    async def set(self, key, value):
        client = redis.Redis(connection_pool=self.pool)
        await client.set(key, value)

    async def get(self, key):
        client = redis.Redis(connection_pool=self.pool)
        value = await client.get(key)
        return value if value else None

    async def put_queue(self, person):
        client = redis.Redis(connection_pool=self.pool)
        await client.lpush("insert", person)

    async def get_queue_len(self):
        client = redis.Redis(connection_pool=self.pool)
        return await client.llen("insert")

    async def get_queue_range(self, len):
        persons = []
        client = redis.Redis(connection_pool=self.pool)
        for i in range(len):
            _, person = await client.brpop("insert")
            persons.append(pickle.loads(person))
        return persons


cache = Cache()
