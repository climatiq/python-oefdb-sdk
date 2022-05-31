from __future__ import annotations

import typing

from pydantic import BaseModel, Field

from oefdb.validators.schema.cell_validators import CellValidator


class ColumnSchema(BaseModel):
    column_name: str = Field(alias="name")
    validators: typing.List[CellValidator]
    allow_empty: bool

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

        all_errors = {}

        for validator in self.validators:
            error = validator.validate_cell(cell_value)
            if error:
                all_errors[validator.validator_name] = error

        if all_errors:
            return all_errors
        return None

    def fix_cell(self, cell_value: str) -> None | str:
        """
        Fix a cell.

        Returns None for a valid cell, or an updated cell value for a cell that could be fixed
        """
        # Do not attempt to fix empty cells if they are allowed
        if cell_value == "" and self.allow_empty:
            return None

        original_cell_value = cell_value
        # This might break at some point if we have fixers that are incompatible, as the "latest" fixer
        # supplied will "win" and the user will get the message that the problem was fixed even though the cell
        # still won't validate. I think that's okay.
        for validator in self.validators:
            fix_result = validator.fix_cell(cell_value)
            if fix_result is None:
                pass
            else:
                cell_value = fix_result

        if original_cell_value == cell_value:
            return None
        return cell_value
