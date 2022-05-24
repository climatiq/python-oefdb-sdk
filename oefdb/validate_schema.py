from __future__ import annotations

import csv
import traceback
from typing import Dict

import click
import pydantic
from pandas import DataFrame

from oefdb.schema_validation.configuration import ColumnSchema
from oefdb.util.from_oefdb_csv import from_oefdb_csv_raw
from oefdb.validators._typing import validator_result_type
from oefdb.validators.check_for_duplicates import check_for_duplicates
from oefdb.validators.check_ids_for_unsupported_characters import (
    check_ids_for_unsupported_characters,
)
from oefdb.validators.check_oefdb_structure import check_oefdb_structure

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
def cli(schema: str, input: str) -> None:
    try:
        try:
            schema = ColumnSchema.load_schema_definition(schema)
        except pydantic.ValidationError as e:
            print("Error loading TOML file")
            print(e)
            exit(1)

        oefdb_csv = from_oefdb_csv_raw(input)

        headers = oefdb_csv[0]
        rows = oefdb_csv[1:]

        print(headers)
        print(rows[0])

        validation_result, errors = schema.validate_headers(headers)
        if validation_result is False:
            print("ERROR VALIDATING COLUMN STRUCTURE")
            print("Please edit the column schema.")
            print("Errors:")

            format_errors(errors)

            for e in errors:
                print(e)
            exit(1)

        validation_result, errors = schema.validate_rows(rows)
        print(validation_result, errors)
        if validation_result is False:
            print("ERROR VALIDATING COLUMN STRUCTURE")
            print("Please edit the column schema.")
            print("Errors:")

            format_errors(errors)

            for e in errors:
                print(e)
            exit(1)

        exit(0)
    except Exception as e:
        print("Exception when running command", e)
        print(traceback.format_exc())
        exit(1)


def format_errors(error_structure):
    for (row, errors) in error_structure():
        print("--------------------------")
        print(f"Error in row {row}")

        print("\n\n\n")
