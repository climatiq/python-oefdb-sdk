from __future__ import annotations

import traceback
from typing import Dict

import click
import pydantic
from click import echo

from oefdb.util.from_oefdb_csv import from_oefdb_csv_raw
from oefdb.validators._typing import validator_result_type
from oefdb.validators.schema.schema import Schema
from oefdb.validators.schema.validation_result import RowErrorsType

results_from_validators_type = Dict[str, validator_result_type]


@click.command()
@click.option(
    "--schema",
    "-s",
    required=True,
    type=click.Path(exists=True),
    help="Schema.toml to use to validate the CSV file",
)
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True),
    help="OEFDB CSV file to validate",
)
def validate_schema_cli_command(schema: str, input: str) -> None:
    try:
        try:
            schema = Schema.load_schema_definition(schema)
        except pydantic.ValidationError as e:
            echo("Error loading TOML file")
            echo(e)
            exit(1)

        oefdb_csv = from_oefdb_csv_raw(input)

        validation_result = schema.validate_all(oefdb_csv)

        if validation_result.column_errors:
            echo("ERROR VALIDATING COLUMN STRUCTURE")
            echo("Please edit the column schema.")
            echo("Errors:")
            for e in validation_result.column_errors:
                echo(e)

            exit(1)

        if validation_result.row_errors:
            echo("ERROR VALIDATING SOME ROWS")
            echo("Errors:")

            output_row_errors(validation_result.row_errors)
            exit(1)

        exit(0)
    except Exception as e:
        echo("---Internal exception when running command---" "")
        echo(f"{e}")
        echo(traceback.format_exc())
        exit(1)


def output_row_errors(errors: RowErrorsType):
    for row_number, columns in errors.items():
        echo(f"--- Error(s) found at row {row_number} ---")
        for column_name, validators in columns.items():
            for validator_name, error in validators.items():
                echo(
                    f"Error found in column '{column_name}' by validator: '{validator_name}': {error}"
                )
        echo()  # newline
