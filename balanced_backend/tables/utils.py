import sys

from balanced_backend.tables.series import PoolSeriesTableType, TokenSeriesTableType


def get_pool_series_table(table_suffix: str) -> PoolSeriesTableType:
    Table: PoolSeriesTableType = getattr(
        sys.modules['balanced_backend.tables'].series,
        "PoolSeries" + table_suffix)
    return Table


def get_token_series_table(table_suffix: str) -> TokenSeriesTableType:
    Table: PoolSeriesTableType = getattr(
        sys.modules['balanced_backend.tables'].series,
        "TokenSeries" + table_suffix)
    return Table
