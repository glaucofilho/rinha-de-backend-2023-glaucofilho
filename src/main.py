import logging

from fastapi import FastAPI

from api.v1.api import api_router
from core.configs import settings
from core.create_tables import create_tables

app = FastAPI()
logging.getLogger("fastapi").setLevel(settings.app_config["LOG_LEVEL"])
if settings.app_config["DISABLE_DOCS"]:
    app.docs_url = None
    app.redoc_url = None
app.include_router(api_router, prefix="")


if __name__ == "__main__":
    import asyncio

    import uvicorn

    asyncio.run(create_tables())
    uvicorn.run(
        "main:app",
        host=settings.app_config["API_HOST"],
        port=settings.app_config["API_PORT"],
        log_level=eval(f'logging.{settings.app_config["LOG_LEVEL"]}'),
        workers=settings.app_config["WORKERS"],
    )
