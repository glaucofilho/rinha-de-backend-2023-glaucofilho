from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from models.pessoas import PessoaModel
from schemas.pessoas import PessoaSchema

router = APIRouter()


class MyRequest(BaseModel):
    my_field: int = Field(..., description="An integer field")


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
    try:
        nascimento = datetime.strptime(pessoa.nascimento, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=422)
    pessoa_model = PessoaModel(
        apelido=pessoa.apelido,
        nome=pessoa.nome,
        nascimento=nascimento,
        stack=pessoa.stack,
    )
    try:
        async with db as session:
            async with session.begin():
                session.add(pessoa_model)
    except IntegrityError:
        raise HTTPException(status_code=422)

    response.headers.update({"Location": f"/pessoas/{pessoa_model.id}"})
