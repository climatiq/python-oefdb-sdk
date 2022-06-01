from __future__ import annotations

import typing

from pydantic import BaseModel, Field

from oefdb.validators.schema.cell_validators import CellValidator


class ColumnSchema(BaseModel):
    column_name: str = Field(alias="name")
    validators: typing.List[CellValidator]
    allow_empty: bool
    allowed_values: typing.Union[None, typing.List[str]]

    def validate_cell(self, cell_value: str) -> None | dict[str, str]:
        """
        Validate a cell.

        Returns None for a valid cell, or a dictionary of errors
        where the keys are the validator names, and the values are the error messages from the validator.
        """
        if cell_value == "":
            if self.allow_empty:
                return None
            else:
                return {
                    "allow_empty": "The cell was empty, but empty cells are not allowed."
                }

        # print(self.allowed_values)
        if self.allowed_values:
            if cell_value not in self.allowed_values:
                return {
                    "allowed_values": f"The value '{cell_value}' was not part of the 'allowed_values' list. Please edit the cell or the list of allowed values."
                }

        all_errors = {}

        for validator in self.validators:
            error = validator.validate_cell(cell_value)
            if error:
                all_errors[validator.validator_name] = error

        if all_errors:
            return all_errors
        return None

    def fix_cell(self, cell_value: str) -> typing.Union[None, str]:
        """
        Fix a cell.

        Returns None for a valid or unfixable, or a string representing the updated value.
        """
        # Do not attempt to fix empty cells if they are allowed
        if cell_value == "" and self.allow_empty:
            return None

        # If the cell is already valid, do not attempt to fix it
        if self.validate_cell(cell_value) is None:
            return None

        original_cell_value = cell_value
        # TODO
        # This might break at some point if we have fixers that are incompatible, as the "latest" fixer
        # supplied will "win" and the user will get the message that the problem was fixed even though the cell
        # still won't validate. We have so few fixers that this might not ever become a problem.
        for validator in self.validators:
            fix_result = validator.fix_cell(cell_value)
            if fix_result is None:
                pass
            else:
                cell_value = fix_result

        if original_cell_value == cell_value:
            return None
        return cell_value
