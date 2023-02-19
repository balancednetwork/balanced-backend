import json

from balanced_backend.utils.api import get_token_transfers_in_blocks, get_logs_in_blocks
from balanced_backend.utils.pools import get_cached_pool_decimals
from balanced_backend.addresses import addresses
from balanced_backend.tables.dex import DexSwap
from balanced_backend.config import settings


def get_token_volume(address: str, block_start: int, block_end: int) -> float:
    token_transfers = get_token_transfers_in_blocks(
        address=address,
        block_start=block_start,
        block_end=block_end,
    )

    volume = sum([i['value_decimal'] for i in token_transfers])
    return volume


def get_swaps(
        block_start: int,
        block_end: int,
) -> list[DexSwap]:
    token_transfers = get_logs_in_blocks(
        address=addresses.DEX_CONTRACT_ADDRESS,
        method="Swap",
        block_start=block_start,
        block_end=block_end,
    )

    swaps: list[DexSwap] = []

    for i in token_transfers:
        data = json.loads(i['data'])
        indexed_data = json.loads(i['indexed'])[1:]

        pool_id = int(indexed_data[0], 16)
        pool_decimals = get_cached_pool_decimals(pool_id=pool_id)

        base_token = indexed_data[1]
        quote_token = pool_decimals['quote_address']

        from_token = data[0]
        to_token = data[1]

        from_value = data[4]
        to_value = data[5]

        # Determine if from_value is base or quote
        if from_token == pool_decimals['base_address']:
            from_decimals = pool_decimals['base_decimals']
            to_decimals = pool_decimals['quote_decimals']
            from_value_decimal = int(from_value, 16) / 10 ** from_decimals
            to_value_decimal = int(to_value, 16) / 10 ** to_decimals
            quote_token_value = to_value
            quote_token_value_decimal = to_value_decimal
            base_token_value = from_value
            base_token_value_decimal = from_value_decimal
        else:
            from_decimals = pool_decimals['quote_decimals']
            to_decimals = pool_decimals['base_decimals']
            from_value_decimal = int(from_value, 16) / 10 ** from_decimals
            to_value_decimal = int(to_value, 16) / 10 ** to_decimals
            quote_token_value = from_value
            quote_token_value_decimal = from_value_decimal
            base_token_value = to_value
            base_token_value_decimal = to_value_decimal

        lp_fees = data[7]
        baln_fees = data[8]
        pool_base = data[9]
        pool_quote = data[10]
        ending_price = data[11]
        effective_fill_price = data[12]

        lp_fees_decimal = int(lp_fees, 16) / 1e18
        baln_fees_decimal = int(baln_fees, 16) / 1e18
        pool_base_decimal = int(pool_base, 16) / 10 ** pool_decimals['base_decimals']
        pool_quote_decimal = int(pool_quote, 16) / 10 ** pool_decimals[
            'quote_decimals']
        ending_price_decimal = int(ending_price, 16) / 10 ** pool_decimals[
            'pool_decimals']
        effective_fill_price_decimal = int(effective_fill_price, 16) / 10 ** \
                                        pool_decimals['pool_decimals']

        swap = DexSwap(
            transaction_hash=i['transaction_hash'],
            chain_id=settings.CHAIN_ID,
            log_index=i['log_index'],
            block_number=i['block_number'],
            pool_id=int(indexed_data[0], 16),
            base_token=base_token,
            quote_token=quote_token,
            from_token=from_token,
            to_token=to_token,
            sender=data[2],
            receiver=data[3],
            from_value=from_value,
            to_value=to_value,
            timestamp=int(int(data[6], 16) / 1e6),
            lp_fees=lp_fees,
            baln_fees=baln_fees,
            pool_base=pool_base,
            pool_quote=pool_quote,
            ending_price=ending_price,
            effective_fill_price=effective_fill_price,
            from_value_decimal=from_value_decimal,
            to_value_decimal=to_value_decimal,
            lp_fees_decimal=lp_fees_decimal,
            baln_fees_decimal=baln_fees_decimal,
            pool_base_decimal=pool_base_decimal,
            pool_quote_decimal=pool_quote_decimal,
            ending_price_decimal=ending_price_decimal,
            effective_fill_price_decimal=effective_fill_price_decimal,
            quote_token_value=quote_token_value,
            quote_token_value_decimal=quote_token_value_decimal,
            base_token_value=base_token_value,
            base_token_value_decimal=base_token_value_decimal,
        )

        swaps.append(swap)

    return swaps
