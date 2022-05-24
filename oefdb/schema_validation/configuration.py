from __future__ import annotations

import pprint
import typing
from typing import List, Optional

import toml
from pydantic import BaseModel, Field, validator

from oefdb.schema_validation.cell_validators import ALL_VALIDATORS
from oefdb.validators._typing import validator_result_type


class CellValidator(BaseModel):
    validator_name: str
    validator_function: typing.Callable[[str], validator_result_type]

    def validate(self, obj) -> validator_result_type:
        return self.validator_function(obj)


class ColumnConfiguration(BaseModel):
    name: str
    validator_strings: list[str] = Field(alias="validators")
    allow_empty: bool
    legal_values: str | None = None

    def validators(self) -> list[CellValidator]:
        return [
            CellValidator(
                validator_name=validator_name,
                validator_function=ALL_VALIDATORS[validator_name],
            )
            for validator_name in self.validator_strings
        ]

    @validator("validator_strings")
    def check_validator_is_defined(cls, v):
        for validator in v:
            if validator not in ALL_VALIDATORS:
                keys = list(ALL_VALIDATORS.keys())
                raise ValueError(
                    f"Wrong validator '{validator}' provided. Validator must one of: {keys}"
                )
        return v

    """
    Returns
    """

    def validate_cell(self, cell) -> (bool, dict):
        if cell == "" and self.allow_empty:
            print("Accepting empty cell")
            return True, []

        # todo better errors
        all_errors = {}

        for validator in self.validators():
            valid, errors = validator.validate(cell)
            if valid:
                pass
            else:
                all_errors[f"{validator.validator_name}"] = errors

        pprint.pp(all_errors)
        if all_errors:
            return False, all_errors
        return True, all_errors


class ColumnSchema(BaseModel):
    columns: list[ColumnConfiguration]

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
    def load_schema_definition(file_path: str) -> ColumnSchema:
        with open(file_path) as f:
            toml_fle = f.read()

        configuration = toml.loads(toml_fle)

        columns = [ColumnConfiguration(**conf) for conf in configuration["columns"]]

        return ColumnSchema(columns=columns)
