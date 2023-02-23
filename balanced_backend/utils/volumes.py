from balanced_backend.utils.api import get_token_transfers_in_blocks


def get_token_volume(address: str, block_start: int, block_end: int) -> float:
    token_transfers = get_token_transfers_in_blocks(
        address=address,
        block_start=block_start,
        block_end=block_end,
    )

    volume = sum([i['value_decimal'] for i in token_transfers])
    return volume
