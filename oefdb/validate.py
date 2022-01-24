from typing import List, Tuple

from pandas import DataFrame

from oefdb.validators.check_for_duplicates import check_for_duplicates
from oefdb.validators.check_ids_for_unsupported_characters import (
    check_ids_for_unsupported_characters,
)
from oefdb.validators.check_oefdb_structure import check_oefdb_structure


def validate(oefdb_df: DataFrame) -> Tuple[bool, dict[str, Tuple[bool, List[str]]]]:

    # run validations
    results_from_validators = {
        "check_for_duplicates": check_for_duplicates(oefdb_df),
        "check_ids_for_unsupported_characters": check_ids_for_unsupported_characters(
            oefdb_df
        ),
        "check_oefdb_structure": check_oefdb_structure(oefdb_df),
    }

    # return the overall validation results, together with explanations
    overall_validation_result = True
    for validator_name, validator_results in results_from_validators.items():
        validation_result, validation_messages = validator_results
        if validation_result is False:
            overall_validation_result = False

    return overall_validation_result, results_from_validators
