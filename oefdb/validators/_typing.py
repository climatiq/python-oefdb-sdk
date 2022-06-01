from __future__ import annotations

import typing
from typing import List, Tuple

validator_result_type = Tuple[bool, List[str]]

"""Rows of a CSV file - each row is a list of strings. The first row is the header row"""
CsvRows = List[List[str]]


"""The return type of cell-validators. Either an error string, or None if the cell is valid."""
cell_validator_return_type = typing.Union[str, None]
