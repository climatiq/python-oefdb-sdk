from __future__ import annotations

import csv
import pathlib
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
@click.option('--fix/--no-fix', default=False, help="Write --fix to attempt to fix any issues that have automatic fixes before validating. This will modify the input file in place.")
def validate_schema_cli_command(schema: str, input: str, fix: bool) -> None:
    try:
        try:
            schema = Schema.load_schema_definition(schema)
        except pydantic.ValidationError as e:
            echo("Error loading TOML file")
            echo(e)
            exit(1)

        oefdb_csv = from_oefdb_csv_raw(input)

        # Check the column structure before doing anything (also applying fixes) because otherwise we'll get weird
        # errors
        schema_errors = schema.validate_headers(oefdb_csv[:1])
        if schema_errors:
            echo("ERROR VALIDATING COLUMN STRUCTURE")
            echo("Please edit the column schema.")
            echo("Errors:")
            for error in schema_errors:
                echo(error)

        if fix:
            fix_result = schema.fix_all(oefdb_csv)

            if fix_result.changes_applied():
                echo("FIXES APPLIED!")
                for change in fix_result.changed_rows:
                    echo(f"Applied fixes on row {change}")


                # First write backup file
                backup_file = pathlib.Path(input).with_suffix(".backup")
                with open(backup_file, "w+") as backup_file:
                    echo(f"Writing a backup file of the input before modifying to {backup_file.name}")
                    writer = csv.writer(backup_file)
                    writer.writerows(oefdb_csv)

                # Then rewrite the original file
                with open(input, "w+") as csvfile:
                    print("Writing back to file", csvfile.name)
                    writer = csv.writer(csvfile)
                    writer.writerows(fix_result.rows_with_fixes())
                    print("finished writing back to file")

            oefdb_csv = fix_result.rows_with_fixes()


        # Validate after fixes
        validation_result = schema.validate_all(oefdb_csv)

        # We should never have column errors here as we've already checked it, but we do it here as a safeguard
        # just in case fixing something broke the column structure in some weird way.
        if validation_result.column_errors:
            echo("ERROR VALIDATING COLUMN STRUCTURE")
            echo("Please edit the column schema.")
            echo("Errors:")
            for error in validation_result.column_errors:
                echo(error)

            exit(1)

        if validation_result.row_errors:
            echo("ERROR VALIDATING SOME ROWS")
            echo("Errors:")

            output_row_errors(validation_result.row_errors)
            exit(1)

        echo("Everything looks good!")
        exit(0)
    except Exception as error:  # noqa:B902
        echo("---Internal exception when running command---" "")
        echo(f"{error}")
        echo(traceback.format_exc())
        exit(1)


def output_row_errors(errors: RowErrorsType) -> None:
    for row_number, columns in errors.items():
        echo(f"--- Error(s) found at row {row_number} ---")
        for column_name, validators in columns.items():
            for validator_name, error in validators.items():
                echo(
                    f"Error found in column '{column_name}' by validator: '{validator_name}': {error}"
                )
        echo()  # newline
