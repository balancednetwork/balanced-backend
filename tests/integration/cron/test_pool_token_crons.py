from balanced_backend.cron.pool_lists import run_pool_list
from balanced_backend.tables.pools import Pool
from sqlmodel import select


def test_get_pools(db):
    with db as session:
        run_pool_list(session=db)
        result = session.execute(select(Pool))
        pools = result.scalars().all()

    assert len(pools) > 30

