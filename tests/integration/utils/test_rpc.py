import pytest
from balanced_backend.utils.rpc import (
    ReachableNotValidException,
    convert_hex_int,
    get_pool_id,
    get_icx_call_block_height,
    get_pool_price,
    get_pool_stats,
    get_contract_method_int,
    post_rpc,
    get_icx_total_supply,
    get_band_price,
)
from balanced_backend.addresses import addresses


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


def test_get_pool_price():
    with pytest.raises(ReachableNotValidException):
        get_pool_price(pool_id=61, height=59812104)

    price = get_pool_price(pool_id=61)
    assert isinstance(price, int)


# These are all the contract update blocks
STATS_HEIGHTS = [
    33582638,
    33582788,
    33653148,
    33729322,
    33737128,
    33901353,
    33980981,
    35748690,
    38802010,
    39008934,
    39268803,
    39352074,
    39747797,
    40926490,
    42281806,
    44536712,
    45396500,
    51433143,
    51909391,
    52901160,
    54713801,
    58036066,
    58640633,
    58855781,
    60876175,
    60927398,
]


@pytest.mark.parametrize("height", STATS_HEIGHTS)
def test_get_pool_stats_and_nonce_over_range(height):
    """
    Test that the getStats and getNonce methods have existed through all the updates on
    the dex contract.
    """
    stats = get_pool_stats(pool_id=1, height=height)
    assert isinstance(stats, dict)

    nonce = get_contract_method_int(
        to_address=addresses.DEX_CONTRACT_ADDRESS,
        method='getNonce',
        height=height,
    )
    assert isinstance(nonce, int)


def test_get_pool_id():
    pool = get_pool_id(
        base_address="cx2609b924e33ef00b648a409245c7ea394c467824",
        quote_address="cx88fd7df7ddff82f7cc735c871dc519838cb235bb"
    )

    assert pool == 2


def test_get_tx_result():
    r = post_rpc(
        payload={
            "jsonrpc": "2.0",
            "id": 1234,
            "method": "icx_getTransactionResult",
            "params": {
                "txHash": "0x036dc1dd5ee5d4c2ef4758e1c5c367b45598922088023b0f881bdc2fda42c469"
            },
        }
    )
    x = r.json()
    print()


def test_get_icx_total_supply():
    total_supply = get_icx_total_supply()
    assert isinstance(total_supply, int)


def test_get_band_price():
    """Verified these prices against CMC roughly."""
    price = get_band_price(symbol='ICX')
    assert price
    price = get_band_price(symbol='ICX', height=50000000)
    assert price
    price = get_band_price(symbol='ICX', height=33585760)
    assert price
