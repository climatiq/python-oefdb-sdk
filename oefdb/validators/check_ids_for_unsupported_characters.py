from pandas import DataFrame

from oefdb.validators._typing import validator_result_type


def check_ids_for_unsupported_characters(df: DataFrame) -> validator_result_type:
    """
    Check ids for unsupported characters.

    Function to check for unsupported characters in the ids
    (currently IDs consist of alphanumeric characters and
    "-", "_", "." (hyphens, underscroes and dots))

    Parameters
    ----------
    df : OEFDB dataframe to be checked for funny characters in the id column

    Returns
    ----------
    wrong_char_ids - a snippet of OEFDB whre ids contain unsupported characters

    and prints out IDs to be checked and their respective numbers
    ----------
    """
    validation_messages = []

    if "activity_id" not in df.columns:
        validation_messages.append("No ID column found")
        return False, validation_messages

    wrong_char_ids = df[
        ~df["activity_id"].replace({r"-|_|\.": ""}, regex=True).str.isalnum()
    ]
    if len(wrong_char_ids) == 0:
        validation_messages.append("IDs look good! There are no funny characters found")
        return True, validation_messages

    validation_messages.append(
        "\n"
        + "\n"
        + "Check the following IDs for unsupported characters:"
        + "\n"
        + "\n"
        + str(wrong_char_ids.activity_id.unique())
        + "\n"
        + "\nin lines:"
        + "\n"
        + str(list(wrong_char_ids.index + 2))
        + "\n"
    )
    return False, validation_messages
