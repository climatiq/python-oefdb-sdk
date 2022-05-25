from __future__ import annotations

import csv
from typing import Any

from pandas import DataFrame, read_csv

from oefdb.validators._typing import CsvRows


def from_oefdb_csv(
    filepath_or_buffer: Any,
) -> DataFrame:
    return read_csv(filepath_or_buffer=filepath_or_buffer)


def from_oefdb_csv_raw(
    path: str,
) -> CsvRows:
    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)
