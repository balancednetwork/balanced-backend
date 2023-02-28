import json
import requests
from typing import Optional

from balanced_backend.config import settings
from balanced_backend.log import logger
from balanced_backend.addresses import addresses


def convert_hex_int(hex_string: str) -> int:
    return int(hex_string, 16)


def post_rpc_json(response):
    if response.status_code != 200:
        return None
    return response.json()["result"]


def post_rpc(payload: dict):
    r = requests.post(settings.ICON_NODE_URL, data=json.dumps(payload))

    # TODO: Remove?
    if r.status_code != 200:
        logger.info(f"Error {r.status_code} with payload {payload}")
        r = requests.post(settings.BACKUP_ICON_NODE_URL, data=json.dumps(payload))
        if r.status_code != 200:
            logger.info(f"Error {r.status_code} with payload {payload} to backup")
        return r

    return r


def get_icx_call_block_height(params: dict, height: int = None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": params,
    }

    if height is not None:
        payload['params']['height'] = hex(height)

    return post_rpc(payload)


def get_icx_call(to_address: str, params: dict, height: int = None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": to_address,
            "dataType": "call",
            "data": params
        },
    }
    if height is not None:
        payload['params']['height'] = hex(height)

    return post_rpc(payload)


def get_contract_method_str(to_address: str, method: str) -> str:
    r = get_icx_call(
        to_address=to_address, params={'method': method}
    )
    if r.status_code == 200:
        return r.json()['result']
    else:
        raise Exception(f"RPC endpoint not available for {method} method...")


def get_contract_method_int(to_address: str, method: str, height: int = None) -> int:
    r = get_icx_call(
        to_address=to_address, params={'method': method}, height=height
    )
    if r.status_code == 200:
        return int(r.json()['result'], 16)
    else:
        raise Exception(f"RPC endpoint not available for {method} method...")


def get_pool_id(base_address: str, quote_address: str) -> int:
    r = get_icx_call(
        to_address=addresses.DEX_CONTRACT_ADDRESS,
        params={
            'method': 'getPoolId',
            'params': {
                '_token1Address': base_address,
                '_token2Address': quote_address,
            }
        }
    )
    if r.status_code == 200:
        return int(r.json()['result'], 16)
    raise Exception(
        f"DEX contract unreachable for token1={base_address} and/or for "
        f"token2={quote_address}..."
    )


class ReachableNotValidException(Exception):
    pass


def get_pool_price(
        pool_id: int,
        height: Optional[int] = None,
):
    r = get_icx_call_block_height(
        params={
            'to': addresses.DEX_CONTRACT_ADDRESS,
            "dataType": "call",
            "data": {
                "method": "getBasePriceInQuote",
                "params": {
                    "_id": str(pool_id)
                }
            }
        },
        height=height
    )
    if r.status_code == 200:
        return int(r.json()['result'], 16)
    elif r.status_code == 400:
        raise ReachableNotValidException()
    raise Exception(
        f"DEX contract for poolId={pool_id} unreachable for get base price..."
    )


def get_pool_stats(pool_id: int, height: int = None) -> Optional[dict]:
    params = {
        'method': 'getPoolStats',
        'params': {
            '_id': str(pool_id)
        }
    }
    if height is not None:
        params['height'] = hex(height)

    r = get_icx_call(
        to_address=addresses.DEX_CONTRACT_ADDRESS,
        params=params
    )
    if r.status_code == 200:
        return r.json()['result']
    raise Exception(
        f"DEX contract for poolId={pool_id} unreachable for get stats..."
    )


def get_band_price(symbol: str, height: int = None) -> float:
    """Band contract was updated from python to java at the below block height."""
    if height is None or height > 59878978:
        address = addresses.BAND_REF_CONTRACT_ADDRESS
        method = 'getRefData'
        param_name = 'symbol'
    else:
        address = addresses.BAND_CONTRACT_ADDRESS_PYTHON
        method = 'get_ref_data'
        param_name = '_symbol'

    r = get_icx_call(
        to_address=address,
        params={
            'method': method,
            'params': {
                param_name: symbol
            }
        },
        height=height,
    )
    if r.status_code == 200:
        return int(r.json()['result']['rate'], 16) / 1e9
    raise Exception(
        f"Band contract for symbol={symbol} unreachable for get ref..."
    )


def get_last_block() -> int:
    r = post_rpc(payload={
        "jsonrpc": "2.0",
        "method": "icx_getLastBlock",
        "id": 1234
    })
    if r.status_code == 200:
        return r.json()['result']['height']
    raise Exception(
        f"Could not get the last block height..."
    )


def get_icx_total_supply():
    r = post_rpc(
        payload={
            "jsonrpc": "2.0",
            "method": "icx_getTotalSupply",
            "id": 1234
        }
    )
    if r.status_code == 200:
        return int(r.json()['result'], 16)
    raise Exception(
        f"Could not get the last block height..."
    )
