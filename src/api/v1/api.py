from fastapi import APIRouter

from api.v1.endpoints import pessoas

api_router = APIRouter()

api_router.include_router(pessoas.router, prefix="", tags=["pessoas"])
