from fastapi import APIRouter

from balanced_backend.api.v1.endpoints import contract_methods
from balanced_backend.api.v1.endpoints import volumes
from balanced_backend.api.v1.endpoints import pools
from balanced_backend.api.v1.endpoints import tokens
from balanced_backend.api.v1.endpoints import holders
from balanced_backend.api.v1.endpoints import cmc
from balanced_backend.api.v1.endpoints import coingecko
from balanced_backend.api.v1.endpoints import stats


api_router = APIRouter()
api_router.include_router(contract_methods.router)
api_router.include_router(volumes.router)
api_router.include_router(pools.router)
api_router.include_router(tokens.router)
api_router.include_router(holders.router)
api_router.include_router(cmc.router, prefix='/coin-market-cap', tags=["coin-market-cap"])
api_router.include_router(coingecko.router, prefix='/coingecko', tags=["coingecko"])
api_router.include_router(stats.router)
