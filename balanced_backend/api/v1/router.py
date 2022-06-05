from fastapi import APIRouter

from balanced_backend.api.v1.endpoints import loans_chart

api_router = APIRouter()
api_router.include_router(loans_chart.router)
