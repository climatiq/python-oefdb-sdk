from __future__ import annotations

from typing import List, Tuple

validator_result_type = Tuple[bool, List[str]]

"""Rows of a CSV file - each row is a list of strings. The first row is the header row"""
CsvRows = List[List[str]]
