import pickle
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.agent import insert_queue
from core.cache import cache
from core.deps import get_session
from core.query import BUSCA_PESSOA_SQL, CONSULTA_PESSOA_SQL
from models.pessoas import PessoaModel
from schemas.pessoas import (CreatePessoaSchema, PessoaSchema,
                             ReturnPessoaSchema)

router = APIRouter()


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
    pessoa: CreatePessoaSchema,
):
    cached_result = await cache.get(pessoa.apelido)
    if cached_result is not None:
        raise HTTPException(status_code=422)
    pessoa = PessoaSchema(**pessoa.dict())
    pessoa_model = {
        "id": pessoa.id,
        "apelido": pessoa.apelido,
        "nome": pessoa.nome,
        "nascimento": pessoa.nascimento.isoformat(),
        "stack": pessoa.stack,
        "busca": f"{pessoa.apelido} {pessoa.nome} {' '.join(pessoa.stack) if pessoa.stack else ''}",
    }
    await cache.set(str(pessoa.id), pickle.dumps(pessoa_model))
    await cache.set(pessoa_model["apelido"], 0)
    await insert_queue.put(pessoa_model)
    response.headers.update({"Location": f"/pessoas/{pessoa.id}"})


@router.get("/pessoas/{pessoa_id}", response_model=ReturnPessoaSchema)
async def detalhe_pessoa(
    pessoa_id: UUID,
):
    cached_result = await cache.get(str(pessoa_id))
    if cached_result:
        cached_result = pickle.loads(cached_result)
        del cached_result["busca"]
        return Response(content=str(cached_result))
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
