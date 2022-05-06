from __future__ import annotations

from pandas import DataFrame

from oefdb.validators._typing import validator_result_type


def check_for_empty_uuids(df: DataFrame) -> validator_result_type:
    """ """
    validation_messages: list[str] = []

    return False, validation_messages
