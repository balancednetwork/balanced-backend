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
]
