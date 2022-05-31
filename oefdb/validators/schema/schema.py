from __future__ import annotations

import pprint
import typing
from typing import List

import tomli
from pydantic import BaseModel

from oefdb.validators._typing import CsvRows
from oefdb.validators.schema.cell_validators import ALL_VALIDATORS
from oefdb.validators.schema.column_schema import ColumnSchema
from oefdb.validators.schema.validation_result import SchemaValidationResult, SchemaFixResult


class Schema(BaseModel):
    columns: List[ColumnSchema]

    def _validate_single_row(self, row: List[str]) -> dict[str, dict[str, str]]:
        all_errors = {}

        for (cell, column) in zip(row, self.columns):
            error = column.validate_cell(cell)
            if error:
                all_errors[column.column_name] = error

        return all_errors

    def _fix_single_row(self, row: List[str]) -> typing.Union[None, List[str]]:
        """Return None if the row is unchanged, or an entire new row with some cells changed."""
        row_changed = False
        updated_row = []
        for (cell, column) in zip(row, self.columns):
            new_value = column.fix_cell(cell)
            print("new value", new_value)
            if new_value:
                updated_row.append(new_value)
                row_changed = True
            else:
                updated_row.append(cell)

        if row_changed:
            return updated_row
        else:
            return None

    def validate_headers(self, headers: List[str]) -> List[str]:
        errors = []

        for index, column in enumerate(self.columns):
            try:
                if headers[index] != column.column_name:
                    errors.append(
                        f"Expected column {index + 1} to be '{column.column_name}', but got '{headers[index]}'"
                    )
            except IndexError:
                errors.append(
                    f"Expected column {index + 1} to be '{column.column_name}', but found no column"
                )

        if len(self.columns) < len(headers):
            surplus = headers[len(self.columns):]
            errors.append(
                f"Got more columns than expected. Please delete the extra columns or configure your schema file with the extra columns: {surplus}"
            )

        return errors

    def validate_all(self, csv: CsvRows) -> SchemaValidationResult:
        headers = csv[0]
        column_errors = self.validate_headers(headers)
        # If we have issues with the header structure it doesn't make much sense to try to parse rows
        # so we just return early
        if column_errors:
            return SchemaValidationResult(column_errors=column_errors, row_errors={})

        rows = csv[1:]

        row_errors = {}
        for index, row in enumerate(rows):
            # We don't have the header here,  so we need to skip 1, and 1 more as a CSV is 1-indexed
            csv_index = index + 2

            error = self._validate_single_row(row)
            if error:
                row_errors[csv_index] = error

        return SchemaValidationResult(
            column_errors=column_errors, row_errors=row_errors
        )

    def fix_all(self, csv: CsvRows) -> SchemaFixResult:
        """
        Attempts to fix all rows in the CSV file.

        It is expected that you have validated the schema before calling this method.
         """
        rows = csv[1:]

        updated_rows = []
        rows_that_were_changed = []
        for index, row in enumerate(rows):
            # We don't have the header here,  so we need to skip 1, and 1 more as a CSV is 1-indexed
            csv_index = index + 2
            print("row", index, row)

            changed_value = self._fix_single_row(row)

            print('changed value', changed_value)
            if changed_value:
                updated_rows.append(changed_value)
                rows_that_were_changed.append(csv_index)
            else:
                updated_rows.append(row)

        all_rows_fixed = csv[0:1] + updated_rows

        print('changed rows')
        pprint.pp(rows_that_were_changed)

        print('rows with fixed values')
        pprint.pp(all_rows_fixed)

        return SchemaFixResult(
            changed_rows=rows_that_were_changed,
            rows_with_fixed_values=all_rows_fixed
        )

    @staticmethod
    def load_schema_definition(file_path: str) -> Schema:
        with open(file_path) as f:
            toml_string = f.read()

        return Schema.from_toml_string(toml_string)

    @staticmethod
    def from_toml_string(toml_schema: str) -> Schema:
        configuration = tomli.loads(toml_schema)

        columns = []
        try:
            for conf in configuration["columns"]:
                validators = [ALL_VALIDATORS[v] for v in conf["validators"]]

                pprint.pp(conf)
                pprint.pp(validators)
                columns.append(ColumnSchema(**{**conf, "validators": validators}))

            return Schema(columns=columns)
        except KeyError as e:
            print("Error while parsing configuration", e)
            print("Configuration loaded from file: ")
            print(configuration)
            raise
