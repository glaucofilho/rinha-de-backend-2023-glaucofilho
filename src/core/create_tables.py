
from core.db import get_database_connection
from core.config import DBBaseModel

async def create_tables() -> None:
    from models.pessoas import Pessoa
    print("Criando as tabelas no banco de dados...")
    async with get_database_connection.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.drop_all)
        await conn.run_sync(DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso.')
    

if __name__ == '__main__':
    import asyncio
    
    asyncio.run(create_tables())