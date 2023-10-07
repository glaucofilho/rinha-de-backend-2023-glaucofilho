from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import PlainTextResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from core.deps import get_session
from models.pessoas import PessoaModel
from schemas.pessoas import PessoaSchema

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
    response: Response, pessoa: PessoaSchema, db: AsyncSession = Depends(get_session)
):
    try:
        nascimento_date = datetime.strptime(pessoa.nascimento, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Invalid date format. Please use 'YYYY-MM-DD' format for the date.",
        )

    pessoa_model = PessoaModel(
        apelido=pessoa.apelido,
        nome=pessoa.nome,
        nascimento=nascimento_date,
        stack=pessoa.stack,
    )
    try:
        async with db as session:
            async with session.begin():
                session.add(pessoa_model)

    # Except caso ja exista um apelido
    except IntegrityError:
        raise HTTPException(status_code=422)

    response.headers.update({"Location": f"/pessoas/{pessoa_model.id}"})
