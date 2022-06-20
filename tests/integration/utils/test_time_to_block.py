from balanced_backend.utils.time_to_block import get_block_from_timestamp, get_timestamp_from_block


def test_get_block_from_timestamp():
    height = get_block_from_timestamp(1654408655811470)
    assert height == 50941047


def test_get_timestamp_from_block():
    timestamp = get_timestamp_from_block(50941046)
    assert timestamp == 1654408653732543


def test_timestamp_and_block():
    timestamp = 1654408653732543
    block = 50941046

    block_out = get_block_from_timestamp(timestamp)
    timestamp_out = get_timestamp_from_block(block_out)
    assert timestamp_out == timestamp
    assert block == block_out

