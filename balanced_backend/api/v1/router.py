from fastapi import APIRouter

from balanced_backend.api.v1.endpoints import historical

api_router = APIRouter()
api_router.include_router(historical.router)
