from pandas import DataFrame


def check_for_duplicates(df: DataFrame) -> bool:
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
    dupl_oefdb = df[
        df.duplicated(subset=["id", "year", "region", "source", "unit"], keep=False)
    ].reset_index()
    if len(dupl_oefdb) == 0:
        print("All good! There are no duplicates in the OEFDB")
        return True
    dupl_oefdb["line_number"] = dupl_oefdb["index"] + 2
    dupl_line_numbers = (
        dupl_oefdb.groupby(["id", "year", "region", "source", "unit"])
        .apply(lambda x: list(x.line_number))
        .reset_index(name="line_number")
    )
    print("Total number of duplicates in the OFEDB: ", len(dupl_oefdb))
    return False
