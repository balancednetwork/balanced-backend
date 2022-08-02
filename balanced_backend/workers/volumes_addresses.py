from balanced_backend.addresses import addresses

daily_volumes = [
    {
        'contract_name': 'loans',
        'address': addresses.LOANS_CONTRACT_ADDRESS,
        'method': 'FeePaid',
        'indexed_position': 1,
        'init_chart_time': 1619308800,
        'decimals': 1e18,
    },
    {
        'contract_name': 'bnusd',
        'address': addresses.BNUSD_CONTRACT_ADDRESS,
        'method': 'Transfer',
        'indexed_position': 2,
        'init_chart_time': 1619308800,
        'decimals': 1e18,
    },
    {
        'contract_name': 'loans',
        'address': addresses.LOANS_CONTRACT_ADDRESS,
        'method': 'OriginateLoan',
        'indexed_position': 2,
        'init_chart_time': 1619308800,
        'decimals': 1e18,
    },
    {
        'contract_name': 'sicx',
        'address': addresses.SICX_CONTRACT_ADDRESS,
        'method': 'Transfer',
        'indexed_position': 2,
        'init_chart_time': 1619308800,
        'decimals': 1e18,
    },
    {
        'contract_name': 'baln',
        'address': addresses.BALANCED_TOKEN_CONTRACT_ADDRESS,
        'method': 'Transfer',
        'indexed_position': 2,
        'init_chart_time': 1619308800,
        'decimals': 1e18,
    },
    {
        'contract_name': 'loans',
        'address': addresses.LOANS_CONTRACT_ADDRESS,
        'method': 'Rebalance',
        'indexed_position': 3,
        'init_chart_time': 1619308800,
        'decimals': 1e18,
    },
]
