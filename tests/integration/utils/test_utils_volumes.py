from balanced_backend.utils.volumes import get_token_volume


def test_get_token_volume():
    volume = get_token_volume(
        address="cx88fd7df7ddff82f7cc735c871dc519838cb235bb",  # bnusd
        block_start=50000000,
        block_end=50000000 + 10000,
    )
    assert volume > 300000
