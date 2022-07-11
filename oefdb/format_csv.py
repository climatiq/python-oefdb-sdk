from __future__ import annotations

import csv
import filecmp
import shutil
import traceback
from typing import Dict

import click
import pandas
from click import echo

from oefdb.validators._typing import validator_result_type

results_from_validators_type = Dict[str, validator_result_type]


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
        # Read the original csv
        with open(input, newline="") as csvfile:
            reader = csv.reader(csvfile)
            csv_rows = pandas.read_csv(csvfile, dtype=str, keep_default_na=False)

        sort_order = ["sector", "category", "name", "region", "year_released", "source", "UUID"]
        sort_ascending = [True, True, True, True, False, True, True]
        csv_rows.sort_values(by=sort_order, ascending=sort_ascending, inplace=True, key=lambda col: col.str.lower())

        print(csv_rows)


        # Write the new csv out to a temporary file
        # This is to make it easier to ensure that newlines
        # are correct when comparing files
        # writing to a StringIO seems to not be consistent with newline handling
        temporary_file = f"{input}.formatting"
        with open(
            temporary_file,
            "w",
            encoding="utf-8",
            newline="",
        ) as f:
            csv_rows.to_csv(f, quoting=csv.QUOTE_NONE, line_terminator="\n", index=False)

        if filecmp.cmp(input, temporary_file, shallow=False):
            echo("Formatting okay!")
        else:
            echo("Formatting not okay. Formatting CSV in-place")

        # Override regular file with temporary file
        # If they're not identical this fixes the formatting
        # If they are identical, this does nothing (apart from modifying the files modified time)
        shutil.move(temporary_file, input)

    except Exception as error:  # noqa:B902
        echo("---Internal exception when running command---" "")
        echo(f"{error}")
        echo(traceback.format_exc())
        exit(1)
