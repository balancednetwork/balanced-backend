from balanced_backend.utils.rpc import (
    convert_hex_int,
    post_rpc_json,
    loans_getTotalCollateral,
    bnusd_totalSupply,
)


def test_get_loans_amount():
    loans_amount = post_rpc_json(loans_getTotalCollateral(40000000))
    loans_amount_int = convert_hex_int(loans_amount) / 1e18
    assert loans_amount == '0x2aaa1b77d33a3a1d826693'
    assert round(loans_amount_int, 8) > 51578193.0  # sanity


def test_bnusd_totalSupply():
    value = post_rpc_json(bnusd_totalSupply(40000000))
    loans_amount_int = convert_hex_int(value) / 1e18
    assert value == '0xeb4e5b6423c4c871b518f'
    assert round(loans_amount_int, 8) > 17779224.0  # sanity
