import asyncio
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from psycopg_pool import AsyncConnectionPool

from api.v1.api import api_router
from core.agent import worker
from core.configs import settings
from core.create_tables import create_tables

if settings.app_config["DISABLE_DOCS"]:
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI()
logging.getLogger("fastapi").setLevel(settings.app_config["LOG_LEVEL"])

app.include_router(api_router, prefix="")


@app.on_event("startup")
async def setup_db_pool():
    pool = AsyncConnectionPool(
        conninfo=settings.DATABASE_URL_POOL,
        max_size=settings.POOL_MAX_SIZE,
        min_size=settings.POOL_MIN_SIZE,
        max_idle=settings.POOL_IDLE,
    )
    asyncio.create_task(worker(pool))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    req: Request, exc: RequestValidationError
):
    errors = exc.errors()

    if any(
        error["type"] == "string_type" and isinstance(error["input"], int)
        for error in errors
    ):
        return Response(status_code=400)

    return Response(status_code=422)


if __name__ == "__main__":
    import uvicorn

    asyncio.run(create_tables())
    uvicorn.run(
        "main:app",
        host=settings.app_config["API_HOST"],
        port=settings.app_config["API_PORT"],
        log_level=eval(f'logging.{settings.app_config["LOG_LEVEL"]}'),
        workers=settings.app_config["WORKERS"],
    )
