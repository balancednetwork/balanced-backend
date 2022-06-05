import json

import requests

from balanced_backend.config import settings
from balanced_backend.log import logger


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


def get_icx_call(to_address: str, params: dict):
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
    return post_rpc(payload)



def get_loans_amount():
    payload = {
        "jsonrpc": "2.0",
        "id": 1234,
        "method": "icx_call",
        "params": {
            "to": settings.LOANS_CONTRACT_ADDRESS,
            "dataType": "call",
            "data": {"method": "getTotalCollateral"}
        },
    }
    return post_rpc(payload)
