from pydantic import BaseModel, Field
from typing import Optional


# CRIANDO O SCHEMA DE PESSOA UTILIANDO OS PARAMETROS DE REFERENCIA E LIMITE
class PessoaSchema(BaseModel):
    apelido: str = Field(..., max_length=32, example="GlaucoSixx")
    nome: str = Field(..., max_length=100, example="Glauco")
    nascimento: str = Field(..., max_length=10, example="1900-01-01")
    stack: list[str] = Field(..., max_length=32, example=["Python", "FastAPI"])
