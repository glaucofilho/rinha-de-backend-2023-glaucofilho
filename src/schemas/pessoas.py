from datetime import date
from typing import Optional
import uuid

from pydantic import BaseModel, Field


class PessoaSchema(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    apelido: str = Field(..., max_length=32, example="GlaucoSixx")
    nome: str = Field(..., max_length=100, example="Glauco")
    nascimento: date = Field(..., example=date(1900, 1, 1))
    stack: Optional[list[str]] = Field(
        ..., max_length=32, example=["Python", "FastAPI"]
    )


class ReturnPessoaSchema(BaseModel):
    id: uuid.UUID
    apelido: str = Field(..., max_length=32, example="GlaucoSixx")
    nome: str = Field(..., max_length=100, example="Glauco")
    nascimento: date = Field(..., example=date(1900, 1, 1))
    stack: Optional[list[str]] = Field(
        ..., max_length=32, example=["Python", "FastAPI"]
    )
