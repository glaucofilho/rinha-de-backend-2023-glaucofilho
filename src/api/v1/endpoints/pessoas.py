from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import PlainTextResponse
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.cache import Cache
from core.deps import get_session
from models.pessoas import PessoaModel
from schemas.pessoas import PessoaSchema, ReturnPessoaSchema

router = APIRouter()

cache = Cache()


CONSULTA_PESSOA_SQL = text(
    "SELECT id, apelido, nome, nascimento, "
    "stack FROM pessoas p WHERE p.id = :id LIMIT 1"
)

BUSCA_PESSOA_SQL = text(
    "SELECT id, apelido, nome, nascimento, "
    "stack FROM pessoas p WHERE p.busca ILIKE :t LIMIT 50"
)

INSERIR_PESSOA_SQL = text(
    "INSERT INTO pessoas (apelido, nome, nascimento, stack, busca) "
    "VALUES (:apelido, :nome, :nascimento, :stack, :busca) "
    "RETURNING id"
)


@router.get("/contagem-pessoas", response_class=PlainTextResponse)
async def contar_pessoas(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PessoaModel)
        result = await session.execute(query)
        pessoas: List[PessoaModel] = result.scalars().all()

        return str(len(pessoas))


@router.post("/pessoas", status_code=201)
async def criar_pessoa(
    response: Response,
    pessoa: PessoaSchema,
):
    cached_result = await cache.get(pessoa.apelido)
    if cached_result is not None:
        raise HTTPException(status_code=422)
    pessoa_model = {
        "apelido": pessoa.apelido,
        "nome": pessoa.nome,
        "nascimento": pessoa.nascimento.isoformat(),
        "stack": pessoa.stack,
        "busca": (
            f"{pessoa.apelido} {pessoa.nome}" f" {' '.join(pessoa.stack)}"
        ),
    }
    try:
        async with get_session() as session:
            result = await session.execute(
                INSERIR_PESSOA_SQL,
                pessoa_model,
            )
    except IntegrityError:
        raise HTTPException(status_code=422)
    row = result.fetchone()
    del pessoa_model["busca"]
    id = str(row[0])
    pessoa_model["id"] = id
    await cache.set(id, str(pessoa_model))
    await cache.set(pessoa_model["apelido"], 0)
    response.headers.update({"Location": f"/pessoas/{id}"})


@router.get("/pessoas/{pessoa_id}", response_model=ReturnPessoaSchema)
async def detalhe_pessoa(
    pessoa_id: UUID,
):
    cached_result = await cache.get(str(pessoa_id))
    if cached_result:
        return Response(content=cached_result)
    async with get_session() as session:
        result = await session.execute(CONSULTA_PESSOA_SQL, {"id": pessoa_id})
        pessoa: PessoaModel = result.fetchone()
        if not pessoa:
            raise HTTPException(status_code=404)
        return pessoa


@router.get("/pessoas", response_model=list[ReturnPessoaSchema])
async def buscar_pessoas(
    t: str = Query(description="Termo de busca", default=None),
):
    if not t:
        raise HTTPException(status_code=400)
    async with get_session() as session:
        result = await session.execute(BUSCA_PESSOA_SQL, {"t": f"%{t}%"})
        pessoas: list[PessoaModel] = result.fetchall()
        return pessoas
