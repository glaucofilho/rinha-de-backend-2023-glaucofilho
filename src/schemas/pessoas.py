from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class PessoaSchema(BaseModel):
    apelido: str = Field(..., max_length=32, example="GlaucoSixx")
    nome: str = Field(..., max_length=100, example="Glauco")
    nascimento: date = Field(..., example=date(1900, 1, 1))
    stack: list[str] = Field(..., max_length=32, example=["Python", "FastAPI"])


class ReturnPessoaSchema(BaseModel):
    id: UUID
    apelido: str = Field(..., max_length=32, example="GlaucoSixx")
    nome: str = Field(..., max_length=100, example="Glauco")
    nascimento: date = Field(..., example=date(1900, 1, 1))
    stack: list[str] = Field(..., max_length=32, example=["Python", "FastAPI"])
