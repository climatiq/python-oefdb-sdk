from typing import Tuple

from pandas import DataFrame


def check_for_duplicates(df: DataFrame) -> Tuple[bool, list[str]]:
    """
    Check for duplicates.

    Function to check for non-unique (i.e. entries with identical
    id, year, region, source and unit values) entries
    in the OEfDB dataframe

    Parameters
    ----------
    df : OEFDB dataframe to be checked for duplicated entries

    Returns
    ----------
    dupl_oefdb        - snippet of the original OEFDB containing duplicated entries only
    dupl_line_numbers - dataframe with non-unique entries and
                        respective line numbers in the original .csv

    and prints the total number of non-unique entries
    ----------
    """
    validation_messages = []

    dupl_oefdb = df[
        df.duplicated(subset=["id", "year", "region", "source", "unit"], keep=False)
    ].reset_index()
    if len(dupl_oefdb) == 0:
        validation_messages.append("All good! There are no duplicates in the OEFDB")
        return True, validation_messages
    dupl_oefdb["line_number"] = dupl_oefdb["index"] + 2
    dupl_line_numbers = (
        dupl_oefdb.groupby(["id", "year", "region", "source", "unit"])
        .apply(lambda x: list(x.line_number))
        .reset_index(name="line_number")
    )
    validation_messages.append(
        f"Total number of duplicates in the OFEDB: {len(dupl_oefdb)}."
        f"Line numbers: {str(dupl_line_numbers)}"
    )
    return False, validation_messages
