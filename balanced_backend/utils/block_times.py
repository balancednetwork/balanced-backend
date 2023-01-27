from datetime import datetime

from balanced_backend.utils.time_to_block import get_block_from_timestamp


def get_block_times() -> (int, int, int):
    current_timestamp = datetime.now().timestamp()

    timestamp_24h = current_timestamp - 86400
    timestamp_7d = current_timestamp - 86400 * 7
    timestamp_30d = current_timestamp - 86400 * 30

    block_height_24h = get_block_from_timestamp(int(timestamp_24h * 1e6))
    block_height_7d = get_block_from_timestamp(int(timestamp_7d * 1e6))
    block_height_30d = get_block_from_timestamp(int(timestamp_30d * 1e6))

    return block_height_24h, block_height_7d, block_height_30d
