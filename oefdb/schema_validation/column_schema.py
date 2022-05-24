from __future__ import annotations

import typing

import pydantic
from pydantic import BaseModel, Field

from oefdb.schema_validation.cell_validators import ALL_VALIDATORS, CellValidator


class ColumnSchema(BaseModel):
    column_name: str = Field(alias="name")
    validator_strings: list[str] = Field(alias="validators")
    allow_empty: bool
    legal_values: typing.Union[str, None] = None  # TODO implement this later

    @pydantic.validator("validator_strings")
    def check_validator_is_legal_value(cls, v):
        for validator in v:
            if validator not in ALL_VALIDATORS:
                keys = list(ALL_VALIDATORS.keys())
                raise ValueError(
                    f"Wrong validator '{validator}' provided. Validator must one of: {keys}"
                )
        return v

    def validators(self) -> list[CellValidator]:
        return [
            CellValidator(
                validator_name=validator_name,
                validator_function=ALL_VALIDATORS[validator_name],
            )
            for validator_name in self.validator_strings
        ]

    def validate_cell(self, cell) -> typing.Union[None, dict[str, str]]:
        """
        Validates a cell. Returns None for a valid cell, or a dictionary of errors
        where the keys are the validator names, and the values are the error messages from the validator.
        """
        if cell == "" and self.allow_empty:
            return None

        all_errors = {}

        for validator in self.validators():
            error = validator.validate_cell(cell)
            if error:
                all_errors[validator.validator_name] = error

        if all_errors:
            return all_errors
        return None
