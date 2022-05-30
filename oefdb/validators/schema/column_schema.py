from __future__ import annotations

from typing import List

import pydantic
from pydantic import BaseModel, Field

from oefdb.validators.schema.cell_validators import ALL_VALIDATORS, CellValidator


class ColumnSchema(BaseModel):
    column_name: str = Field(alias="name")
    validator_strings: List[str] = Field(alias="validators")
    allow_empty: bool

    @pydantic.validator("validator_strings")
    def check_validator_exists(cls, v: str) -> str:
        for validator in v:
            if validator not in ALL_VALIDATORS:
                keys = list(ALL_VALIDATORS.keys())
                raise ValueError(
                    f"Wrong validator '{validator}' provided. Validator must one of: {keys}"
                )
        return v

    def validators(self) -> List[CellValidator]:
        return [
            CellValidator(
                validator_name=validator_name,
                validator_function=ALL_VALIDATORS[validator_name],
            )
            for validator_name in self.validator_strings
        ]

    def validate_cell(self, cell_value: str) -> None | dict[str, str]:
        """
        Validate a cell.

        Returns None for a valid cell, or a dictionary of errors
        where the keys are the validator names, and the values are the error messages from the validator.
        """
        if cell_value == "" and self.allow_empty:
            return None

        all_errors = {}

        for validator in self.validators():
            error = validator.validate_cell(cell_value)
            if error:
                all_errors[validator.validator_name] = error

        if all_errors:
            return all_errors
        return None