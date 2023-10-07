from pydantic import BaseModel, Field


# CRIANDO O SCHEMA DE PESSOA UTILIANDO OS PARAMETROS DE REFERENCIA E LIMITE
class PessoaSchema(BaseModel):
    apelido: str = Field(..., max_length=32)
    nome: str = Field(..., max_length=100)
    nascimento: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    stack: list[str] = Field(..., max_length=32)
