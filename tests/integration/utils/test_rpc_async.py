import asyncio

from balanced_backend.utils.rpc_async import (
    get_pool_stats_async,
    get_total_supply_async,
)


def test_get_pool_stats_async():
    pool_stats = asyncio.run(get_pool_stats_async(pool_ids=[1, 2, 3], height=60000000))

    p2_total_supply_0 = [i for i in pool_stats if i['pool_id'] == 1][0]['total_supply']

    assert isinstance(pool_stats, list)
    assert pool_stats[0]['base_decimals']
    assert pool_stats[0]['pool_id'] == 1

    pool_stats = asyncio.run(get_pool_stats_async(pool_ids=[1, 2, 3], height=61000000))
    p2_total_supply_1 = [i for i in pool_stats if i['pool_id'] == 1][0]['total_supply']

    assert isinstance(pool_stats, list)
    assert pool_stats[0]['base_decimals']
    assert pool_stats[0]['pool_id'] == 1
    assert p2_total_supply_1 != p2_total_supply_0


def test_get_total_supply_async():
    # Pool 4 at this BH was throwing error
    total_supplies = asyncio.run(get_total_supply_async(
        pool_ids=[1, 2, 3, 4], height=38444962
    ))

    assert total_supplies
