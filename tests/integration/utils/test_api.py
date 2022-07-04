from balanced_backend.utils.api import get_logs_in_blocks


def test_get_logs_in_blocks():
    events = get_logs_in_blocks(
        address="cx66d4d90f5f113eba575bf793570135f9b10cece1",
        method="FeePaid",
        block_start=51660434 - 100000,
        block_end=51660434,
    )

    assert len(events) == 138
