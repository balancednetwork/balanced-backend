from balanced_backend.utils.pools import get_cached_pool_id, get_cached_pool_decimals, POOL_IDS, POOL_DECIMALS


def test_get_cached_pool_id():
    pool_id = get_cached_pool_id(
        base_address="cx2609b924e33ef00b648a409245c7ea394c467824",
        quote_address="cx88fd7df7ddff82f7cc735c871dc519838cb235bb"
    )
    assert pool_id == 2
    assert POOL_IDS[
               "cx2609b924e33ef00b648a409245c7ea394c467824" +
               "cx88fd7df7ddff82f7cc735c871dc519838cb235bb"
               ] == 2

    pool_id = get_cached_pool_id(
        base_address="cx88fd7df7ddff82f7cc735c871dc519838cb235bb",
        quote_address="cx2609b924e33ef00b648a409245c7ea394c467824"
    )
    assert pool_id == 2
    assert POOL_IDS[
               "cx88fd7df7ddff82f7cc735c871dc519838cb235bb" +
               "cx2609b924e33ef00b648a409245c7ea394c467824"
               ] == 2


def test_get_cached_pool_decimals():
    pool_decimals = get_cached_pool_decimals(2)

    assert pool_decimals['base_decimals'] == 18
