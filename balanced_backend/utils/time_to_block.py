import requests
from json import JSONDecodeError

from balanced_backend.config import settings
from balanced_backend.log import logger

def get_block_from_timestamp(timestamp: int):
    r = requests.get(settings.COMMUNITY_API_ENDPOINT + f'/api/v1/blocks/timestamp/{str(timestamp)}')
    if r.status_code == 200:
        try:
            response = r.json()
        except JSONDecodeError:
            logger.info("Invalid response from get_block_from_timestamp, check url.")
            return None
        return response['number']
    else:
        logger.info("Invalid status code from get_block_from_timestamp, check url.")
