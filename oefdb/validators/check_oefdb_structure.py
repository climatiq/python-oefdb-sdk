import numpy as np
from pandas import DataFrame


def check_oefdb_structure(df: DataFrame) -> bool:
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
        print("The header of OEFDB is wrong: please check the file!")
        print(
            "These columns should not be there: {}".format(
                set(df.columns).difference(col)
            )
        )
        print("These columns are missing: {}".format(set(col).difference(df.columns)))
        return False

    if len(df.columns) == len(col):
        print("Number of columns looks good!")

    if (col != df.columns).sum():
        print(
            "Check that headers of the columns:",
            np.where(col != df.columns)[0] + 1,
            "match the correct naming:",
            col[col != df.columns],
        )
        return False

    if (col == df.columns).sum() == len(col):
        print("All headers are intact!")

    return True
