import asyncio

from core.configs import settings
from core.query import insert_into_db

insert_queue = asyncio.Queue()


# async def process_batch(pool, batch):
#     await insert_into_db(pool, batch)


# async def worker(pool):
#     batch_size = settings.BLOCO_TAMANHO
#     batch_timeout = settings.INTERVALO_SEGUNDOS

#     while True:
#         tasks = []
#         while len(tasks) < batch_size:
#             try:
#                 person = await asyncio.wait_for(
#                     insert_queue.get(), timeout=batch_timeout
#                 )
#                 if person:
#                     task = asyncio.create_task(process_batch(pool, [person]))
#                     tasks.append(task)
#             except asyncio.TimeoutError:
#                 break

#         if tasks:
#             await asyncio.gather(*tasks)


# # import asyncio

# # from core.configs import settings
# # from core.query import insert_into_db

# # insert_queue = asyncio.Queue()


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