from pandas import DataFrame

from oefdb.validators._typing import validator_result_type


def check_for_duplicates(df: DataFrame) -> validator_result_type:
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
        df.duplicated(
            subset=[
                "activity_id",
                "year_released",
                "region",
                "source",
                "activity_unit",
                "lca_activity",
            ],
            keep=False,
        )
    ].reset_index()
    if len(dupl_oefdb) == 0:
        validation_messages.append("All good! There are no duplicates in the OEFDB")
        return True, validation_messages
    dupl_oefdb["line_number"] = dupl_oefdb["index"] + 2
    dupl_line_numbers = (
        dupl_oefdb.groupby(
            [
                "activity_id",
                "year_released",
                "region",
                "source",
                "activity_unit",
                "lca_activity",
            ]
        )
        .apply(lambda x: list(x.line_number))
        .reset_index(name="line_number")
    )
    dupl_line_numbers_short = dupl_line_numbers[["activity_id", "line_number"]]
    lines = ["\t".join(dupl_line_numbers_short.columns)]
    for row in dupl_line_numbers_short.values:
        row_str = "\t".join(map(process_row, row))
        lines.append(row_str)
    dupl_line_numbers_str = "\n".join(lines)

    validation_messages.append(
        f"\n"
        f"\nTotal number of duplicates in the OFEDB: {len(dupl_line_numbers)}."
        f"\n"
        f"\n"
        f"{(dupl_line_numbers_str)}"
        # f"{(dupl_line_numbers)}"
        f"\n"
    )
    return False, validation_messages


def process_row(element: DataFrame) -> DataFrame:
    element = str(element)
    if len(element) < 80:
        return element
    else:
        return "{}...".format(element[:80])
