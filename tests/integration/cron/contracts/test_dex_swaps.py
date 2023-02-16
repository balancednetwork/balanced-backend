
from balanced_backend.config import settings
from balanced_backend.cron.contracts.dex_swaps import run_dex_swaps, get_last_swap
from balanced_backend.utils.rpc import get_last_block


def test_run_dex_swaps(db):
    # Usually there is a swap in last 1000 blocks otherwise need to mock get_last_block
    settings.BLOCK_SYNC_CHUNK = 1000
    settings.FIRST_BLOCK = get_last_block() - settings.BLOCK_SYNC_CHUNK
    with db as session:
        run_dex_swaps(session=session)
        swap = get_last_swap(session=session)
    assert swap
