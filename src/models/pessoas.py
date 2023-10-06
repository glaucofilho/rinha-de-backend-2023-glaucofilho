from sqlalchemy import Column, Integer, String, Date, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoas'
    
    id = Column(Integer, primary_key=True, index=True)
    apelido = Column(String(32))
    nome = Column(String(100))
    nascimento = Column(Date)
    stack = Column(ARRAY(String(32)))
