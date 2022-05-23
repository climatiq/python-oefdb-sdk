import csv
import datetime
import itertools
import math
import pprint
import typing
from typing import List, Optional

import toml
from pydantic import BaseModel, Field, validator

from oefdb.new.cell_validators import ALL_VALIDATORS


class ColumnConfiguration(BaseModel):
    name: str
    validator_strings: List[str] = Field(alias="validators")
    allow_empty: bool
    legal_values: Optional[str] = None

    def validators(self):
        return [
            ALL_VALIDATORS[validator_name] for validator_name in self.validator_strings
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

    # todo deal with error messages later
    def validate_cell(self, cell) -> bool:
        if cell == "" and self.allow_empty:
            print("Accepting empty cell")
            return True

        for validator in self.validators():
            valid, errors = validator(cell)
            if valid:
                pass
            else:
                print("!!!!!!!!!!!!!!!!!!!!! NO")
                print(type(cell))
                raise Exception(f"Invalid {errors}")
        return True


class ColumnSchema(BaseModel):
    columns: List[ColumnConfiguration]

    def validate_row(self, row):
        for (cell, column) in zip(row, self.columns):
            print(cell, column)
            column.validate_cell(cell)

    # Todo better error messages
    def validate_header(self, headers):
        for index, column in enumerate(self.columns):
            assert headers[index] == column.name

        assert len(self.columns) == len(headers)


def load_schema_definition(file_path: str) -> ColumnSchema:
    with open(file_path) as f:
        toml_fle = f.read()

    configuration = toml.loads(toml_fle)

    columns = [ColumnConfiguration(**conf) for conf in configuration["columns"]]
    return ColumnSchema(columns=columns)
