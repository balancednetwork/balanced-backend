from balanced_backend.utils.rpc import get_icx_call_block_height


def get_band_icx_price(height: int = None) -> float:
    r = get_icx_call_block_height(
        params={
            "from": "hx23ada4a4b444acf8706a6f50bbc9149be1781e13",
            "to": "cxe647e0af68a4661566f5e9861ad4ac854de808a2",
            "dataType": "call",
            "data": {
                "method": "getReferenceData",
                "params": {
                    "base": "ICX",
                    "quote": "USD"
                }
            }
        },
        height=height,
    )
    print()
    if r.status_code == 200:
        return int(r.json()['result']['rate'], 16) / 1e18
    else:
        raise Exception("Band oracle unreachable. RPC endpoint down.")
