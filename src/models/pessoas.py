from sqlalchemy import ARRAY, Column, Date, String, text
from sqlalchemy.dialects.postgresql import UUID as pgUUID

from core.configs import settings


class PessoaModel(settings.DBBaseModel):
    __tablename__ = "pessoas"

    id = Column(
        pgUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    apelido = Column(String(32), index=True, unique=True)
    nome = Column(String(100))
    nascimento = Column(Date)
    stack = Column(ARRAY(String(32)))
    busca = Column(String, index=True, unique=True)

    def to_json(self):
        return {
            "id": str(self.id),
            "apelido": self.apelido,
            "nome": self.nome,
            "nascimento": str(self.nascimento),
            "stack": self.stack,
        }
