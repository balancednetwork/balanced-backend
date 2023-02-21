import pytest

from balanced_backend.utils.volumes import get_token_volume, get_swaps
from balanced_backend.config import settings

def test_get_token_volume():
    volume = get_token_volume(
        address="cx88fd7df7ddff82f7cc735c871dc519838cb235bb",  # bnusd
        block_start=50000000,
        block_end=50000000 + 10000,
    )
    assert volume > 300000


SWAP_CASES = [
    (61946326, 0, {
        'from_value_decimal': 113,
    })
]


@pytest.mark.parametrize("block,index,checks", SWAP_CASES)
def test_get_swaps(block, index, checks):
    # Need to fix this as the backend randomly shuffles the order of the log depending
    # on location. Related to fix putting composite index on tx index / log index
    settings.COMMUNITY_API_ENDPOINT = "https://tracker.v2.mainnet.sng.vultr.icon.community"

    swaps = get_swaps(
        block_start=block,
        block_end=block,
    )

    for k, v in checks.items():
        expected_value = v
        if isinstance(v, int):
            outcome = int(getattr(swaps[index], k))
        else:
            outcome = getattr(swaps[index], k)

        assert outcome == expected_value
