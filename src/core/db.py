
import asyncpg
from core.config import DATABASE_URL

# FUNCAO GERADORA ASSINCRONA PARA ENTREGAR UMA CONEXAO COM O BANCO
async def get_database_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()