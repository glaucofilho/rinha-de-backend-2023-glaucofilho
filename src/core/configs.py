from os import getenv
from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()


class Settings(BaseSettings):
    """
    Configuracoes gerais usadas na aplicacao
    """

    # PEGANDO ATRIBUTOS PASSADOS PELAS ENVS DO DOCKER-COMPSOE
    _DB_USER: str = getenv("DB_USER", "root")
    _DB_PASS: str = getenv("DB_PASS", "1234")
    _DB_ADDRESS: str = getenv("DB_ADDRESS", "localhost")
    _DB_NAME: str = getenv("DB_NAME", "banco")

    # MONTANDO A URL DE CONEXAO COM O BANCO
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{_DB_USER}:{_DB_PASS}@{_DB_ADDRESS}/{_DB_NAME}"
    )
    DBBaseModel: ClassVar = declarative_base()

    REDIS_ADDRESS: str = getenv("REDIS_ADDRESS", "localhost")
    REDIS_PORT: int = int(getenv("REDIS_PORT", "6379"))

    # CONFIGURACOES DA API
    app_config: dict = {
        "LOG_LEVEL": getenv("LOG_LEVEL", "CRITICAL"),
        "DISABLE_DOCS": getenv("DISABLE_DOCS", "True").lower() == "true",
        "WORKERS": int(getenv("WORKERS", 1)),
        "API_PORT": int(getenv("API_PORT", 8000)),
        "API_HOST": str(getenv("API_HOST", "0.0.0.0")),
    }

    class Config:
        case_sensitive = True


settings = Settings()
