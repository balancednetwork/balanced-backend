from balanced_backend.config import settings



daily_historical = [
    # {
    #     'contract_name': 'loans',
    #     'params': {
    #         "to": settings.LOANS_CONTRACT_ADDRESS,
    #         "dataType": "call",
    #         "data": {"method": "getTotalCollateral"}
    #     },
    #     'init_chart_time': 1619308800,
    # },
    # {
    #     'contract_name': 'bnusd',
    #     'params': {
    #         "to": settings.BNUSD_CONTRACT_ADDRESS,
    #         "dataType": "call",
    #         "data": {"method": "totalSupply"}
    #     },
    #     'init_chart_time': 1619308800,
    # },
    {
        'contract_name': 'staked_icx',
        'params': {
            "to": settings.STAKING_CONTRACT_ADDRESS,
            "dataType": "call",
            "data": {"method": "getTotalSupply"}
        },
        'init_chart_block': 47751328,
    },
]
