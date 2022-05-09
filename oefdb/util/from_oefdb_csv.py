from __future__ import annotations

from typing import Any

from pandas import DataFrame, read_csv


def from_oefdb_csv(
    filepath_or_buffer: Any,
) -> DataFrame:
    return read_csv(filepath_or_buffer=filepath_or_buffer)
