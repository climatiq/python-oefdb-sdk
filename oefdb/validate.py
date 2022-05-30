from __future__ import annotations

from typing import Dict

import click
from pandas import DataFrame

from oefdb.validators._typing import validator_result_type
from oefdb.validators.check_for_duplicates import check_for_duplicates

results_from_validators_type = Dict[str, validator_result_type]


def validate(oefdb_df: DataFrame) -> tuple[bool, results_from_validators_type]:

    # run validations
    results_from_validators: results_from_validators_type = {
        "---------- checking for duplicates ------": check_for_duplicates(oefdb_df),
    }

    # return the overall validation results, together with explanations
    overall_validation_result = True
    for validator_name, validator_results in results_from_validators.items():
        validation_result, validation_messages = validator_results
        if validation_result is False:
            overall_validation_result = False

    return overall_validation_result, results_from_validators


@click.command()
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True),
    help="OEFDB CSV file to validate",
)
def cli(input: str) -> None:
    import oefdb
    from oefdb.util.present_results_from_validators import (
        present_results_from_validators,
    )

    oefdb_df = oefdb.from_oefdb_csv(input)

    oefdb.validate(oefdb_df)

    validation_result, results_from_validators = oefdb.validate(oefdb_df)

    present_results_from_validators(validation_result, results_from_validators)

    if validation_result is False:
        exit(1)
    else:
        exit(0)
