from balanced_backend.cron.method_addresses import contract_methods, update_contract_methods

def test_cron_method_addresses():
    update_contract_methods()

    num_collateral_tokens = 0
    x = contract_methods
    assert contract_methods
