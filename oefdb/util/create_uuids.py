from __future__ import annotations

import uuid

from pandas import DataFrame, isna


def assign_uuids_to_new_entries(df: DataFrame) -> DataFrame:

    for i in range(len(df)):
        if isna(df.loc[i, "UUID"]):
            df.loc[i, "UUID"] = uuid.uuid4()
    return df
