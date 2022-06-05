from balanced_backend.utils.rpc import (
    convert_hex_int,
    post_rpc_json,
)


def test_get_bond():
    # bond = post_rpc_json(get_bond('hx0b047c751658f7ce1b2595da34d57a0e7dad357d'))
    bond = post_rpc_json(get_bond("hx1e15b53379e5ee634a2da493a43fdc2d03d0c718"))
    assert bond
