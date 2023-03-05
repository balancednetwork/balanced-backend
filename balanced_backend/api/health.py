from fastapi import Depends

from balanced_backend.db import get_session
from balanced_backend.cache.cache import cache


def check_database_online(session: bool = Depends(get_session)):
    return session


def check_cmc_cache_updated():
    if len(cache.cmc_trades) == 0:
        return False
    return True
