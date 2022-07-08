from __future__ import annotations

import csv
import pathlib
import traceback
import typing
from typing import Dict

import click
import pydantic
from click import echo

from oefdb.util.from_oefdb_csv import from_oefdb_csv_raw
from oefdb.validators._typing import CsvRows, validator_result_type
from oefdb.validators.schema.schema import Schema
from oefdb.validators.schema.validation_result import RowErrorsType
import io
results_from_validators_type = Dict[str, validator_result_type]
import filecmp
import shutil

@click.command()
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True),
    help="OEFDB CSV file to fix formatting for",
)
def format_csv_cli_command(input: str) -> None:
    try:
        # Read the csv both as rows and as a string
        with open(input, newline="") as csvfile:
            original_csv_string = csvfile.read()
            csvfile.seek(0)
            reader = csv.reader(csvfile)
            csv_rows = list(reader)

        # Write csv out to a temporary file
        temporary_file = f"{input}.formatting"
        with open(temporary_file, "w", encoding="utf-8", newline='',) as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONE, lineterminator="\n")
            writer.writerows(csv_rows)

        if filecmp.cmp(input, temporary_file, shallow=False):
            echo("Formatting not okay. Formatting CSV in-place")
        else:
            echo("Formatting okay! Not doing anything.")

        shutil.move(temporary_file, input)

    except Exception as error:  # noqa:B902
        echo("---Internal exception when running command---" "")
        echo(f"{error}")
        echo(traceback.format_exc())
        exit(1)
