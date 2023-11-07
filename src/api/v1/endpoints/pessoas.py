import json
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import PlainTextResponse
from sqlalchemy import String, cast, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.cache import Cache
from core.deps import get_session
from models.pessoas import PessoaModel
from schemas.pessoas import PessoaSchema, ReturnPessoaSchema

router = APIRouter()

cache = Cache()


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
    db: AsyncSession = Depends(get_session),
):
    cached_result = await cache.get(pessoa.apelido)
    if cached_result is not None:
        raise HTTPException(status_code=422)
    pessoa_model = PessoaModel(
        apelido=pessoa.apelido,
        nome=pessoa.nome,
        nascimento=pessoa.nascimento,
        stack=pessoa.stack,
    )
    try:
        async with db as session:
            async with session.begin():
                session.add(pessoa_model)
    except IntegrityError:
        raise HTTPException(status_code=422)
    await cache.set(str(pessoa_model.id), json.dumps(pessoa_model.to_json()))
    await cache.set(pessoa_model.apelido, True)
    response.headers.update({"Location": f"/pessoas/{pessoa_model.id}"})


@router.get("/pessoas/{pessoa_id}", response_model=ReturnPessoaSchema)
async def detalhe_pessoa(
    pessoa_id: UUID,
    db: AsyncSession = Depends(get_session),
):
    cached_result = await cache.get(str(pessoa_id))
    if cached_result:
        return json.loads(cached_result)
    async with db as session:
        query = select(PessoaModel).where(PessoaModel.id == pessoa_id)
        result = await session.execute(query)
        pessoa: PessoaModel = result.scalar()

        if not pessoa:
            raise HTTPException(status_code=404)

        return pessoa


@router.get("/pessoas", response_model=list[ReturnPessoaSchema])
async def buscar_pessoas(
    t: str = Query(description="Termo de busca", default=None),
    db: AsyncSession = Depends(get_session),
):
    if not t:
        raise HTTPException(status_code=400)

    async with db as session:
        query = (
            select(PessoaModel)
            .filter(
                (
                    func.lower(PessoaModel.apelido).ilike(f"%{t}%")
                    | func.lower(PessoaModel.nome).ilike(f"%{t}%")
                    | cast(PessoaModel.stack, String).ilike(f"%{t}%")
                )
            )
            .limit(50)
        )

        result = await session.execute(query)
        pessoas: list[PessoaModel] = result.scalars().all()

        return pessoas
