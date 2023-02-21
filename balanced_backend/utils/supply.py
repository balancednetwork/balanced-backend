from balanced_backend.utils.rpc import get_contract_method_str, get_icx_total_supply


def get_total_supply(address: str, decimals: int) -> float:
    if address == 'ICX':
        total_supply = get_icx_total_supply() / 10 ** decimals
    else:
        total_supply = int(
            get_contract_method_str(to_address=address, method="totalSupply"),
            16) / 10 ** decimals
    return total_supply
