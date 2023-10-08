import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.v1.api import api_router
from core.configs import settings
from core.create_tables import create_tables

app = FastAPI()
logging.getLogger("fastapi").setLevel(settings.app_config["LOG_LEVEL"])
if settings.app_config["DISABLE_DOCS"]:
    app.docs_url = None
    app.redoc_url = None
app.include_router(api_router, prefix="")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    req: Request, exc: RequestValidationError
):
    details = exc.errors()
    if any(
        detail["type"] == "string_type" and isinstance(detail["input"], int)
        for detail in details
    ):
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder({"detail": details}),
        )
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": details}),
    )


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
