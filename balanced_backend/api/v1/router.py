from fastapi import APIRouter

from balanced_backend.api.v1.endpoints import contract_methods
from balanced_backend.api.v1.endpoints import volumes

api_router = APIRouter()
api_router.include_router(contract_methods.router)
api_router.include_router(volumes.router)
