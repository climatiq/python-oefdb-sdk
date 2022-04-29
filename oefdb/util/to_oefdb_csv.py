from __future__ import annotations

from pandas import DataFrame


def to_oefdb_csv(oefdb_df: DataFrame) -> str:
    return oefdb_df.to_csv(index=False).strip()
