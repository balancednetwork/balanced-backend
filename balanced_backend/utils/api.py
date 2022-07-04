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
    r = requests.get(endpoint)
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
    else:
        logger.info(f"Error getting {endpoint}")
        return None
