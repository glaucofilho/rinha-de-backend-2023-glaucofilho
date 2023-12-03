import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CreatePessoaSchema(BaseModel):
    apelido: str = Field(..., max_length=32)
    nome: str = Field(..., max_length=100)
    nascimento: date # = Field(...)
    stack: Optional[list[str]]  = Field(
        ..., max_length=32
    )


class PessoaSchema(CreatePessoaSchema):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    # stack: Optional[str]


class ReturnPessoaSchema(BaseModel):
    id: uuid.UUID
    apelido: str  # = Field(..., max_length=32, example="GlaucoSixx")
    nome: str  # = Field(..., max_length=100, example="Glauco")
    nascimento: date  # = Field(..., example=date(1900, 1, 1))
    stack: Optional[str]
