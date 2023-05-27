import pytest

from balanced_backend.config import settings
from balanced_backend.utils.dex import get_swaps, get_dex_adds

SWAP_CASES = [
    (61946326, 0, {
        'from_value_decimal': 113,
    })
]


# @pytest.mark.parametrize("block,index,checks", SWAP_CASES)
# def test_get_swaps(block, index, checks):
#     # Need to fix this as the backend randomly shuffles the order of the log depending
#     # on location. Related to fix putting composite index on tx index / log index
#     settings.COMMUNITY_API_ENDPOINT = "https://tracker.v2.mainnet.sng.vultr.icon.community"
#
#     swaps = get_swaps(
#         block_start=block,
#         block_end=block,
#     )
#
#     for k, v in checks.items():
#         expected_value = v
#         if isinstance(v, int):
#             outcome = int(getattr(swaps[index], k))
#         else:
#             outcome = getattr(swaps[index], k)
#
#         assert outcome == expected_value



ADD_CASES = [
    (62298752, 0, {
        'value_decimal': 45,
    })
]


@pytest.mark.parametrize("block,index,checks", ADD_CASES)
def test_get_adds(block, index, checks):
    adds = get_dex_adds(
        block_start=block,
        block_end=block,
    )

    for k, v in checks.items():
        expected_value = v
        if isinstance(v, int):
            outcome = int(getattr(adds[index], k))
        else:
            outcome = getattr(adds[index], k)

        assert outcome == expected_value
