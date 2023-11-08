from time import sleep

from core.configs import settings
from core.database import engine


async def create_tables() -> None:
    from models.pessoas import PessoaModel

    print("Creating tables in the database...")
    sleep(3)
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print("Tables created successfully.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
