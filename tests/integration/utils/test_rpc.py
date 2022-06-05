from balanced_backend.utils.rpc import (
    convert_hex_int,
    post_rpc_json,
    get_loans_amount,
)


def test_get_loans_amount():
    loans_amount = post_rpc_json(get_loans_amount())
    loans_amount_int = convert_hex_int(loans_amount) / 1e18
    assert loans_amount_int > 1000000  # sanity
