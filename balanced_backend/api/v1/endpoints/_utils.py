from asyncio import sleep

from balanced_backend.cache.cache import cache
from balanced_backend.log import logger


async def sleep_while_empty_cache(cache_item):
    while len(getattr(cache, cache_item)) == 0:
        logger.info(f"Early cache request {cache_item}")
        await sleep(1)
