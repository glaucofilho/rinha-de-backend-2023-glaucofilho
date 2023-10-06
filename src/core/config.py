from os import getenv
from sqlalchemy.ext.declarative import declarative_base

# PEGANDO ATRIBUTOS PASSADOS PELAS ENVS DO DOCKER-COMPSOE
_DB_USER = getenv("DB_USER")
_DB_PASS = getenv("DB_PASS")
_DB_ADDRESS = getenv("DB_ADDRESS")
_DB_NAME = getenv("DB_NAME")

# MONTANDO A URL DE CONEXAO COM O BANCO
DATABASE_URL = f"postgresql://{_DB_USER}:{_DB_PASS}@{_DB_ADDRESS}/{_DB_NAME}"

DBBaseModel = declarative_base()