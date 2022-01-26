import numpy as np
from pandas import DataFrame

from oefdb.validators._typing import validator_result_type


def check_oefdb_structure(df: DataFrame) -> validator_result_type:
    """
    Check OEFDB structure.

    Function to check that number of columns is correct and their headers
    are following the oefdb structure, and columns have specific datatype

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
            "id",
            "name",
            "unit",
            "factor",
            "uncertainty",
            "source",
            "year",
            "region",
            "date_accessed",
            "description",
            "source_link",
            "lca_activity",
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
            "These columns are missing: {}".format(set(col).difference(df.columns))
        )
        return False, validation_messages

    if len(df.columns) == len(col):
        validation_messages.append("Number of columns looks good!")

    if (col != df.columns).sum():
        validation_messages.append(
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
        validation_messages.append("All headers are intact!")

    return True, validation_messages
