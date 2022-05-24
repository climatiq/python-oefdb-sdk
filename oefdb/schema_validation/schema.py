from __future__ import annotations

import toml

from oefdb.schema_validation.column_schema import ColumnSchema
from oefdb.validators._typing import validator_result_type


class Schema(BaseModel):
    columns: list[ColumnSchema]

    def validate_single_row(self, row):
        all_errors = {}

        for (cell, column) in zip(row, self.columns):
            # print("cell:", cell, "column:", column)
            valid, errors = column.validate_cell(cell)
            if not valid:
                all_errors[column.name] = errors

        print("row errors", errors)
        if all_errors:
            return False, all_errors
        return True, all_errors

    def validate_rows(self, rows: list[list[str]]):
        errors = {}
        for index, row in enumerate(rows):
            csv_index = (
                index + 2
            )  # We don't have the header here so we need to skip that, and CSV is 1-indexed
            valid, error = self.validate_single_row(row)
            if not valid:
                print("not valid", error)
                errors[csv_index] = error
            else:
                print("valid!", row)

        if errors:
            return False, errors
        return True, errors

    # Todo better error messages
    def validate_headers(self, headers) -> validator_result_type:
        errors = []

        for index, column in enumerate(self.columns):
            try:
                if headers[index] != column.name:
                    errors.append(
                        f"Expected column {index+1} to be '{column.name}', but got '{headers[index]}'"
                    )
            except IndexError:
                errors.append(
                    f"Expected column {index+1} to be '{column.name}', but found no column"
                )

        # If the length is not identical here, it's because there's too many headers
        if len(self.columns) != len(headers):
            surplus = headers[len(self.columns) :]
            errors.append(
                f"Got more columns than expected. Please delete the extra columns or configure your schema file with the extra columns.: {surplus}"
            )

        if errors:
            return False, errors
        else:
            return True, errors

    def validate_all(self, csv: list):
        headers = csv[0]
        valid, error = self.validate_headers(headers)
        if valid is False:
            return valid, error

        rows = csv[1:]

        return self.validate_rows(rows)

    @staticmethod
    def load_schema_definition(file_path: str) -> Schema:
        with open(file_path) as f:
            toml_fle = f.read()

        configuration = toml.loads(toml_fle)

        columns = [ColumnSchema(**conf) for conf in configuration["columns"]]

        return Schema(columns=columns)
