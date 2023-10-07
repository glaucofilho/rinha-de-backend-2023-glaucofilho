from sqlalchemy import ARRAY, Column, Date, Integer, String

from core.configs import settings


class PessoaModel(settings.DBBaseModel):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    apelido = Column(String(32))
    nome = Column(String(100))
    nascimento = Column(Date)
    stack = Column(ARRAY(String(32)))
