from balanced_backend.utils.rpc import (
    convert_hex_int,
    get_icx_call_block_height,
)


def test_get_icx_call_block_height():
    r = get_icx_call_block_height(
        params={
            'to': 'cx88fd7df7ddff82f7cc735c871dc519838cb235bb',
            "dataType": "call",
            "data": {"method": "totalSupply"}
        },
        height=39538474,
    )
    value = convert_hex_int(r.json()['result'])

    assert r.status_code == 200
    assert value == 18713814011765392578046295
