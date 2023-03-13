import requests

from balanced_backend.config import settings
from balanced_backend.log import logger


def get_logs_in_blocks(
        address: str,
        method: str,
        block_start: int,
        block_end: int,
        carry_over: list = None,
        skip: int = 0,
        retries: int = 0,
):
    if carry_over is None:
        carry_over = []
    query_string = f'?address={address}' \
                   f'&method={method}' \
                   f'&block_start={block_start}' \
                   f'&block_end={block_end}' \
                   f'&limit=100' \
                   f'&skip={skip}'
    endpoint = settings.COMMUNITY_API_ENDPOINT + '/api/v1/logs' + query_string
    logger.info(f"GET {endpoint}")
    with requests.get(endpoint) as r:
        if r.status_code == 200:
            output = r.json()

            if len(output) == 100:
                carry_over += output
                return get_logs_in_blocks(
                    address=address,
                    method=method,
                    block_start=block_start,
                    block_end=block_end,
                    carry_over=carry_over,
                    skip=skip + 100,
                )

            return output + carry_over
        elif r.status_code == 204:
            # Case where we have exactly %100 records
            return carry_over
        else:
            retries += 1
            logger.info(f"Error getting {endpoint} with status code {r.status_code}")
            if retries < 5:
                return get_logs_in_blocks(
                    address=address,
                    method=method,
                    block_start=block_start,
                    block_end=block_end,
                    carry_over=carry_over,
                    skip=skip,
                    retries=retries
                )
            else:
                logger.info(f"Error getting {endpoint}")
                raise Exception


def get_transactions_in_blocks(
        address: str,
        method: str,
        block_start: int,
        block_end: int,
        carry_over: list = None,
        skip: int = 0,
        retries: int = 0,
):
    if carry_over is None:
        carry_over = []
    query_string = f'?address={address}' \
                   f'&method={method}' \
                   f'&block_start={block_start}' \
                   f'&block_end={block_end}' \
                   f'&limit=100' \
                   f'&skip={skip}'
    endpoint = settings.COMMUNITY_API_ENDPOINT + '/api/v1/logs' + query_string
    logger.info(f"GET {endpoint}")
    with requests.get(endpoint) as r:
        if r.status_code == 200:
            output = r.json()

            if len(output) == 100:
                carry_over += output
                return get_logs_in_blocks(
                    address=address,
                    method=method,
                    block_start=block_start,
                    block_end=block_end,
                    carry_over=carry_over,
                    skip=skip + 100,
                )

            return output + carry_over
        elif r.status_code == 204:
            # Case where we have exactly %100 records
            return carry_over
        else:
            retries += 1
            logger.info(f"Error getting {endpoint} with status code {r.status_code}")
            if retries < 5:
                return get_logs_in_blocks(
                    address=address,
                    method=method,
                    block_start=block_start,
                    block_end=block_end,
                    carry_over=carry_over,
                    skip=skip,
                    retries=retries
                )
            else:
                logger.info(f"Error getting {endpoint}")
                raise Exception


def get_token_transfers_in_blocks(
        address: str,
        block_start: int,
        block_end: int,
        carry_over: list = None,
        skip: int = 0,
        retries: int = 0,
):
    if carry_over is None:
        carry_over = []
    query_string = f'?token_contract_address={address}' \
                   f'&start_block_number={block_start}' \
                   f'&end_block_number={block_end}' \
                   f'&limit=100' \
                   f'&skip={skip}'
    endpoint = settings.COMMUNITY_API_ENDPOINT + '/api/v1/transactions/token-transfers' + query_string
    logger.info(f"GET {endpoint}")
    with requests.get(endpoint) as r:
        if r.status_code == 200:
            output = r.json()

            if len(output) == 100:
                carry_over += output
                return get_token_transfers_in_blocks(
                    address=address,
                    block_start=block_start,
                    block_end=block_end,
                    carry_over=carry_over,
                    skip=skip + 100,
                )

            return output + carry_over
        elif r.status_code == 204:
            # Case where we have exactly %100 records
            return carry_over
        else:
            retries += 1
            logger.info(f"Error getting {endpoint} with status code {r.status_code}")
            if retries < 5:
                return get_token_transfers_in_blocks(
                    address=address,
                    block_start=block_start,
                    block_end=block_end,
                    carry_over=carry_over,
                    skip=skip,
                    retries=retries
                )
            else:
                logger.info(f"Error getting {endpoint}")
                raise Exception


def get_token_holders(address: str):
    endpoint = settings.COMMUNITY_API_ENDPOINT + \
               '/api/v1/transactions/token-holders/token-contract/' \
               + address
    r = requests.head(endpoint)
    if r.status_code == 200:
        # Within cluster the headers are upper case, outside lower case.. :(
        try:
            return int(dict(r.headers)['x-total-count'])
        except KeyError:
            return int(dict(r.headers)['X-Total-Count'])
    logger.info(f"Making call to {endpoint} resulted in status {r.status_code}...")
    logger.info("API endpoint down for holders...")


def get_icx_stats():
    endpoint = settings.COMMUNITY_API_ENDPOINT + '/api/v1/stats'
    r = requests.get(endpoint)
    if r.status_code == 200:
        return r.json()
    logger.info("API endpoint down for stats...")
