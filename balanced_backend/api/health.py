from fastapi import Depends

from balanced_backend.cache.cache import cache
from balanced_backend.db import get_session
from balanced_backend.log import logger

def is_database_online(session: bool = Depends(get_session)):
    return session


def is_cache_updated():
    for k, v in cache.dict().items():
        if len(v) == 0:
            logger.info(f"Unhealthy cache item {k}")
            return False
    return True
