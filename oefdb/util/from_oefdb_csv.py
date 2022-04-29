from __future__ import annotations

from pandas import DataFrame, read_csv
from pandas._typing import FilePathOrBuffer


def from_oefdb_csv(filepath_or_buffer: FilePathOrBuffer) -> DataFrame:
    return read_csv(filepath_or_buffer=filepath_or_buffer)
