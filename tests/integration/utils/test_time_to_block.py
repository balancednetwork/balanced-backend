from balanced_backend.utils.time_to_block import get_block_from_timestamp


def test_get_block_from_timestamp():
    height = get_block_from_timestamp(1654408655811470)
    assert height == 50941046
