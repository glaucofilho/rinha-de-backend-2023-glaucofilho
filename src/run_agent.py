import time

from psycopg_pool import AsyncConnectionPool

from core.cache import cache
from core.configs import settings
from core.query import insert_into_db


async def main():
    pool = AsyncConnectionPool(
        conninfo=settings.DATABASE_URL_POOL,
        max_size=settings.POOL_MAX_SIZE,
        min_size=settings.POOL_MIN_SIZE,
    )

    queue_size = settings.BLOCO_TAMANHO
    queue_time = settings.INTERVALO_SEGUNDOS
    elapsed_time = 0
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        cache_len = await cache.get_queue_len()
        if (
            cache_len >= queue_size or elapsed_time >= queue_time
        ) and cache_len > 0:
            if cache_len > queue_size:
                len = queue_size
            else:
                len = cache_len
            persons = await cache.get_queue_range(len)
            await insert_into_db(pool, persons)
            elapsed_time = 0
            start_time = time.time()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
