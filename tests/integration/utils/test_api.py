from balanced_backend.utils.api import get_logs_in_blocks, get_token_holders


def test_get_logs_in_blocks():
    events = get_logs_in_blocks(
        address="cx66d4d90f5f113eba575bf793570135f9b10cece1",
        method="FeePaid",
        block_start=51660434 - 100000,
        block_end=51660434,
    )

    assert len(events) == 138


def test_get_logs_in_blocks_rebalance():
    events = get_logs_in_blocks(
        address="cx66d4d90f5f113eba575bf793570135f9b10cece1",
        method="Rebalance",
        block_start=39340509,
        block_end=39390509 + 1000,
    )

    assert len(events) > 1


def test_get_token_holders():
    holders = get_token_holders('cxf61cd5a45dc9f91c15aa65831a30a90d59a09619')
    assert isinstance(holders, int)
