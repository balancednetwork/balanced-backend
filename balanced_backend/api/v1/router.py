from fastapi import APIRouter

from balanced_backend.api.v1.endpoints import historical
from balanced_backend.api.v1.endpoints import volumes

api_router = APIRouter()
api_router.include_router(historical.router)
api_router.include_router(volumes.router)
