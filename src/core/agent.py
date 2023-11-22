import asyncio

from core.configs import settings
from core.query import insert_into_db

insert_queue = asyncio.Queue()


async def worker(pool):
    batch_size = settings.BLOCO_TAMANHO
    batch_timeout = settings.INTERVALO_SEGUNDOS

    while True:
        batch = []
        while len(batch) < batch_size:
            try:
                person = await asyncio.wait_for(
                    insert_queue.get(), timeout=batch_timeout
                )
                if person:
                    batch.append(person)
            except asyncio.TimeoutError:
                break
        if batch:
            await insert_into_db(pool, batch)
