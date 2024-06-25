from loguru import logger

from balanced_backend.addresses import addresses
from balanced_backend.utils.rpc import (
    get_icx_call,
    get_contract_method_str,
    get_contract_method_int,
)

contract_methods: list[dict] = [
    {
        "contract_name": "loans",
        "params": {
            "to": addresses.LOANS_CONTRACT_ADDRESS,
            "dataType": "call",
            "data": {"method": "getTotalCollateral"},
        },
        "init_chart_time": 1619308800,
    },
    {
        "contract_name": "bnusd",
        "params": {
            "to": addresses.BNUSD_CONTRACT_ADDRESS,
            "dataType": "call",
            "data": {"method": "totalSupply"},
        },
        "init_chart_time": 1619308800,
    },
    {
        "contract_name": "staked_icx",
        "params": {
            "to": addresses.SICX_CONTRACT_ADDRESS,
            "dataType": "call",
            "data": {"method": "totalSupply"},
        },
        "init_chart_block": 47751328,
    },
]


def update_contract_methods():
    # Loans balance of tokens
    r = get_icx_call(
        to_address=addresses.LOANS_CONTRACT_ADDRESS,
        params={"method": "getCollateralTokens"},
    )
    if r.status_code == 200:
        loans_collatoral_tokens = r.json()["result"]
        for _, c in loans_collatoral_tokens.items():
            symbol = get_contract_method_str(to_address=c, method="symbol")
            decimals = get_contract_method_int(to_address=c, method="decimals")
            contract_methods.append(
                {
                    "contract_name": f"loans_{symbol}_balance",
                    "params": {
                        "to": c,
                        "dataType": "call",
                        "data": {
                            "method": "balanceOf",
                            "params": {"_owner": addresses.LOANS_CONTRACT_ADDRESS},
                        },
                    },
                    "decimals": decimals,
                    "init_chart_block": 47751328,
                }
            )
    else:
        logger.info("Failed to get loans_collatoral_tokens...")

    # Loans `getTotalCollateralDebt` method
    loans_collateral_debt = [
        # {
        #     "address": "cx5b5a03cb525a1845d0af3a872d525b18a810acb0",
        #     "collateral": "BTCB",
        #     "assetSymbol": "bnUSD",
        # },
        # {
        #     "address": "cx288d13e1b63563459a2ac6179f237711f6851cb5",
        #     "collateral": "ETH",
        #     "assetSymbol": "bnUSD",
        # },
        # {
        #     "address": "cx2609b924e33ef00b648a409245c7ea394c467824",
        #     "collateral": "sICX",
        #     "assetSymbol": "bnUSD",
        # },
        {
            "address": "cx4297f4b63262507623b6ad575d0d8dd2db980e4e",
            "collateral": "INJ",
            "assetSymbol": "bnUSD",
        },
        {
            "address": "cx2d552c485ec8bcaa75aac02424e2aca6ffdb2f1b",
            "collateral": "BNB",
            "assetSymbol": "bnUSD",
        },
        {
            "address": "cx66a031cc3bd305c76371fb586e93801b948254f0",
            "collateral": "AVAX",
            "assetSymbol": "bnUSD",
        },
    ]

    for c in loans_collateral_debt:
        symbol = get_contract_method_str(to_address=c["address"], method="symbol")
        decimals = get_contract_method_int(to_address=c["address"], method="decimals")
        contract_methods.append(
            {
                "contract_name": f"loans_collateral_debt_{symbol}_bnusd",
                "params": {
                    "to": addresses.LOANS_CONTRACT_ADDRESS,
                    "dataType": "call",
                    "data": {
                        "method": "getTotalCollateralDebt",
                        "params": {
                            "collateral": c["collateral"],
                            "assetSymbol": c["assetSymbol"],
                        },
                    },
                },
                "decimals": decimals,
                "init_chart_block": 47751328,
            }
        )

    # Stability fund balance of tokens
    r = get_icx_call(
        to_address=addresses.STABILITY_FUND_CONTRACT_ADDRESS,
        params={"method": "getAcceptedTokens"},
    )
    if r.status_code == 200:
        stability_accepted_tokens = r.json()["result"]
        for c in stability_accepted_tokens:
            symbol = get_contract_method_str(to_address=c, method="symbol")
            decimals = get_contract_method_int(to_address=c, method="decimals")
            contract_methods.append(
                {
                    "contract_name": f"stability_{symbol}_balance",
                    "params": {
                        "to": c,
                        "dataType": "call",
                        "data": {
                            "method": "balanceOf",
                            "params": {
                                "_owner": addresses.STABILITY_FUND_CONTRACT_ADDRESS
                            },
                        },
                    },
                    "init_chart_block": 47751328,
                    "decimals": decimals,
                }
            )
    else:
        logger.info("Failed to get stability_accepted_tokens...")
