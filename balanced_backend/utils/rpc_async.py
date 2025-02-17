from loguru import logger
import asyncio
import aiohttp
import json

from balanced_backend.config import settings
from balanced_backend.addresses import addresses


async def get_pool_stats_async_resp(session, pool_id: int, height: int = None) -> dict:
    params = {
        'method': 'getPoolStats',
        'params': {
            '_id': str(pool_id)
        }
    }

    data = {
        "jsonrpc": "2.0",
        "id": pool_id,
        "method": "icx_call",
        "params": {
            "to": addresses.DEX_CONTRACT_ADDRESS,
            "dataType": "call",
            "data": params
        },
    }

    if height is not None:
        data['params']['height'] = hex(height)

    async with session.post(
            url=settings.ICON_NODE_URL, data=json.dumps(data)
    ) as response:
        resp = await response.read()

    ret = json.loads(resp)['result']
    ret['pool_id'] = pool_id
    return ret


async def get_pool_stats_async(pool_ids: list[int], height: int = None):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[
            get_pool_stats_async_resp(session, pool_id=i, height=height) for i in
            pool_ids
        ])
    return ret


async def get_total_supply_async_resp(
        session, pool_id: int,
        height: int = None,
) -> dict:
    data = {
        "jsonrpc": "2.0",
        "id": pool_id,
        "method": "icx_call",
        "params": {
            "to": addresses.DEX_CONTRACT_ADDRESS,
            "dataType": "call",
            "data": {
                'method': 'totalSupply',
                'params': {
                    '_id': str(pool_id)
                }
            }
        },
    }

    if height is not None:
        data['params']['height'] = hex(height)

    try:
        async with session.post(
            url=settings.ICON_NODE_URL,
            data=json.dumps(data),
            timeout=4,
            headers={"Content-Type": "application/json", "User-Agent": "backend/1.0"},
        ) as response:
            resp = await response.read()
            total_supply = int(json.loads(resp)['result'], 0)
    except asyncio.exceptions.TimeoutError as e:
        logger.info(f"Timed out for total supply request for pool {pool_id} and block "
                    f"height {height}...")
        total_supply = 0
    except KeyError as e:
        logger.info(f"Got error with jsonrpc post data={data}")
        raise e

    return {'pool_id': pool_id, 'total_supply': total_supply}


async def get_total_supply_async(pool_ids: list[int], height: int = None):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[
            get_total_supply_async_resp(session, pool_id=i, height=height) for i in
            pool_ids
        ])
    return ret
