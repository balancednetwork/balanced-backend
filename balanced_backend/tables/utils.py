import sys

from balanced_backend.tables.volumes import VolumeTableType


def get_table(table_suffix: str) -> VolumeTableType:
    Table: VolumeTableType = getattr(
        sys.modules['balanced_backend.tables'].volumes,
        "VolumeSeries" + table_suffix)
    return Table
