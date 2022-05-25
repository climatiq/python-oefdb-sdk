from __future__ import annotations

import numpy as np
from pandas import DataFrame

from oefdb.validators._typing import validator_result_type


def check_oefdb_structure(df: DataFrame) -> validator_result_type:
    """
    Check OEFDB structure.

    Function to check that number of columns is correct and their headers
    are following the oefdb structure

    Parameters
    ----------
    df : OEFDB dataframe to be checked for duplicated entries

    Returns
    ----------
    Message if the columns and their names are intact,
    if not which columns to check and to which
    name should they comply
    ----------
    """
    validation_messages = []

    col = np.array(
        [
            "sector",
            "category",
            "activity_id",
            "name",
            "activity_unit",
            "kgCO2e-AR5",
            "kgCO2e-AR4",
            "kgCO2",
            "kgCH4",
            "kgN2O",
            "kgCO2e-OtherGHGs-AR5",
            "kgCO2e-OtherGHGs-AR4",
            "uncertainty",
            "scope",
            "lca_activity",
            "source",
            "year_released",
            "years_valid",
            "years_calculated_from",
            "region",
            "data_quality",
            "contributor",
            "date_accessed",
            "description",
            "source_link",
        ]
    )
    if len(df.columns) != len(col):
        validation_messages.append(
            "The header of OEFDB is wrong: please check the file!"
        )
        validation_messages.append(
            f"These columns should not be there: {set(df.columns).difference(col)}"
        )
        validation_messages.append(
            f"These columns are missing: {set(col).difference(df.columns)}"
        )
        return False, validation_messages

    if len(df.columns) == len(col):
        validation_messages.append("Number of columns looks good!")

    if (col != df.columns).sum():
        validation_messages.append(
            "\n" + "\n"
            "Check that headers of the columns:"
            + "\n"
            + str(np.where(col != df.columns)[0] + 1)
            + "\n"
            + "match the correct naming:"
            + "\n"
            + str(col[col != df.columns])
            + "\n"
        )
        return False, validation_messages

    if (col == df.columns).sum() == len(col):
        validation_messages.append("All headers are intact!" "\n")

    return True, validation_messages
