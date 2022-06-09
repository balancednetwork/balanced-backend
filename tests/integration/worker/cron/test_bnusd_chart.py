from balanced_backend.workers.crons.bnusd_supply_chart import build_bnusd_supply


def test_build_bnusd_supply(db):
    with db as session:
        build_bnusd_supply(session=session)
