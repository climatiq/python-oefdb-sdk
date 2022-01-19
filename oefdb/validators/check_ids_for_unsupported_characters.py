from pandas import DataFrame


def check_ids_for_unsupported_characters(df: DataFrame) -> bool:
    """
    Check ids for unsupported characters.

    Function to check for unsupported characters in the ids
    (curretly IDs consist of alphanumeric characters and
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
    wrong_char_ids = df[~df["id"].replace({r"-|_|\.": ""}, regex=True).str.isalnum()]
    if len(wrong_char_ids) == 0:
        print("IDs look good! There are no funny characters found")
        return True

    print(
        "Check the following IDs for unsupported characters: \n",
        wrong_char_ids.id.unique(),
        " \nin lines:",
        list(wrong_char_ids.index + 2),
        sep="\n",
    )
    return False
