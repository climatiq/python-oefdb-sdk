from __future__ import annotations

import pprint
from typing import List, Dict

import toml
from pydantic import BaseModel

from oefdb.schema_validation.column_schema import ColumnSchema
from oefdb.schema_validation.validation_result import SchemaValidationResult
from oefdb.validators._typing import validator_result_type


class Schema(BaseModel):
    columns: list[ColumnSchema]

    def validate_single_row(self, row) -> Dict[str, str]:
        all_errors = {}

        for (cell, column) in zip(row, self.columns):
            error = column.validate_cell(cell)
            if error:
                all_errors[column.column_name] = error

        print("Errors on row:", all_errors)
        return all_errors

    def validate_headers(self, headers) -> list[str]:
        errors = []

        for index, column in enumerate(self.columns):
            try:
                if headers[index] != column.column_name:
                    errors.append(
                        f"Expected column {index+1} to be '{column.column_name}', but got '{headers[index]}'"
                    )
            except IndexError:
                errors.append(
                    f"Expected column {index+1} to be '{column.column_name}', but found no column"
                )

        # If the length is not identical here, it's because there's too many headers
        if len(self.columns) != len(headers):
            surplus = headers[len(self.columns) :]
            errors.append(
                f"Got more columns than expected. Please delete the extra columns or configure your schema file with the extra columns.: {surplus}"
            )

        return errors

    def validate_all(self, csv: list[list[str]]) -> SchemaValidationResult:
        headers = csv[0]
        column_errors = self.validate_headers(headers)
        # If we have issues with the header structure it doesn't make much sense to try to parse rows
        # so we just return early
        if column_errors:
            return SchemaValidationResult(column_errors=column_errors, row_errors={})

        rows = csv[1:]

        row_errors = {}
        for index, row in enumerate(rows):
            csv_index = (
                index + 2
            )  # We don't have the header here,  so we need to skip 1, and 1 more as a CSV is 1-indexed
            error = self.validate_single_row(row)
            if error:
                row_errors[csv_index] = error


        pprint.pp(row_errors)
        return SchemaValidationResult(
            column_errors=column_errors, row_errors=row_errors
        )

    @staticmethod
    def load_schema_definition(file_path: str) -> Schema:
        with open(file_path) as f:
            toml_fle = f.read()

        configuration = toml.loads(toml_fle)

        columns = [ColumnSchema(**conf) for conf in configuration["columns"]]

        return Schema(columns=columns)
