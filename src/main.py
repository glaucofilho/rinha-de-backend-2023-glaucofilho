from fastapi import FastAPI, HTTPException, Query, Depends
from models.pessoas import Pessoa
from core.db import get_database_connection
from core.create_tables import create_tables
import uuid
import asyncpg

app = FastAPI()


@app.post("/pessoas", response_model=uuid.UUID)
async def criar_pessoa(pessoa: Pessoa, conn: asyncpg.Connection = Depends(get_database_connection)):
    # Verifica se o apelido já existe no banco de dados
    query = "SELECT id FROM pessoas WHERE apelido = $1"
    existing_id = await conn.fetchval(query, pessoa.apelido)
    if existing_id is not None:
        raise HTTPException(status_code=422, detail="Apelido já existe")

    # Gera um ID UUID para a nova pessoa
    pessoa_id = uuid.uuid4()

    # Insere a pessoa no banco de dados
    insert_query = """
        INSERT INTO pessoas (id, apelido, nome, nascimento, stack)
        VALUES ($1, $2, $3, $4, $5)
    """
    await conn.execute(insert_query, str(pessoa_id), pessoa.apelido, pessoa.nome, pessoa.nascimento, pessoa.stack)

    return pessoa_id

@app.get("/pessoas/{id}", response_model=Pessoa)
async def obter_pessoa(id: uuid.UUID, conn: asyncpg.Connection = Depends(get_database_connection)):
    # Obtém os detalhes de uma pessoa do banco de dados
    query = "SELECT id, apelido, nome, nascimento, stack FROM pessoas WHERE id = $1"
    pessoa = await conn.fetchrow(query, str(id))
    if pessoa is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")

    return Pessoa(**pessoa)

@app.get("/pessoas", response_model=list[Pessoa])
async def buscar_pessoas(t: str = Query(..., title="Termo de busca"), conn: asyncpg.Connection = Depends(get_database_connection)):
    # Realiza a busca no banco de dados
    query = """
        SELECT id, apelido, nome, nascimento, stack FROM pessoas
        WHERE LOWER(apelido) LIKE $1 OR LOWER(nome) LIKE $1
    """
    resultados = await conn.fetch(query, f"%{t.lower()}%")

    return [Pessoa(**p) for p in resultados]

@app.get("/contagem-pessoas")
async def contar_pessoas(conn: asyncpg.Connection = Depends(get_database_connection)):
    # Obtém o número de registros de pessoas no banco de dados
    query = "SELECT COUNT(*) FROM pessoas"
    count = await conn.fetchval(query)
    return str(count)

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
