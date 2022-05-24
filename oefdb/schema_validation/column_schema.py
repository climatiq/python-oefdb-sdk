from __future__ import annotations

import pprint

from pydantic import BaseModel, Field, validator

from oefdb.schema_validation.cell_validators import ALL_VALIDATORS, CellValidator


class ColumnSchema(BaseModel):
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
