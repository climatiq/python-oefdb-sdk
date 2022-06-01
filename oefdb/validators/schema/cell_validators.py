from __future__ import annotations

import typing

from pydantic import BaseModel

from oefdb.validators._typing import cell_validator_return_type
from oefdb.validators.schema.cell_validator_functions import (
    generate_uuid_if_empty,
    has_no_commas,
    is_ascii,
    is_date,
    is_float_or_not_supplied,
    is_int,
    is_link,
    is_valid_activity_id,
    is_year,
    no_fix_available,
    validate_is_uuid,
)


class CellValidator(BaseModel):
    validator_name: str
    validator_function: typing.Callable[[str], cell_validator_return_type]
    fixer_function: typing.Callable[[str], cell_validator_return_type]

    def validate_cell(self, cell_value: str) -> cell_validator_return_type:
        """
        Validate that a cell passes the given validator test.

        Cell validators return None if no error is relevant, or a string with an error message
        if any errors have occurred
        """
        # See https://github.com/python/mypy/issues/5485 for why we need to ignore the typechecker here
        return self.validator_function(cell_value)  # type: ignore

    def fix_cell(self, cell_value: str) -> typing.Union[str, None]:
        """
        Attempt to fix the value in a given cell.

        This method when called will return None if the cell cannot be fixed, or does not require fixing.
        It will return a string with the new value if the cell can be fixed.
        """
        # See https://github.com/python/mypy/issues/5485 for why we need to ignore the typechecker here
        return self.fixer_function(cell_value)  # type: ignore


HasNoCommasCellValidator = CellValidator(
    validator_name="has_no_commas",
    validator_function=has_no_commas,
    fixer_function=no_fix_available,
)
IsValidActivityIdCellValidator = CellValidator(
    validator_name="is_valid_activity_id",
    validator_function=is_valid_activity_id,
    fixer_function=no_fix_available,
)
IsAsciiCellValidator = CellValidator(
    validator_name="is_ascii",
    validator_function=is_ascii,
    fixer_function=no_fix_available,
)
IsDateCellValidator = CellValidator(
    validator_name="is_date",
    validator_function=is_date,
    fixer_function=no_fix_available,
)
IsLinkCellValidator = CellValidator(
    validator_name="is_link",
    validator_function=is_link,
    fixer_function=no_fix_available,
)
IsYearCellValidator = CellValidator(
    validator_name="is_year",
    validator_function=is_year,
    fixer_function=no_fix_available,
)
IsFloatOrNotSuppliedCellValidator = CellValidator(
    validator_name="is_float_or_not_supplied",
    validator_function=is_float_or_not_supplied,
    fixer_function=no_fix_available,
)
IsIntCellValidator = CellValidator(
    validator_name="is_int", validator_function=is_int, fixer_function=no_fix_available
)
IsUUIDCellValidator = CellValidator(
    validator_name="is_uuid",
    validator_function=validate_is_uuid,
    fixer_function=generate_uuid_if_empty,
)


# Mapping of strings in the schema file to the corresponding CellValidators
ALL_VALIDATORS = {
    "has_no_commas": HasNoCommasCellValidator,
    "is_valid_activity_id": IsValidActivityIdCellValidator,
    "is_ascii": IsAsciiCellValidator,
    "is_date": IsDateCellValidator,
    "is_link": IsLinkCellValidator,
    "is_year": IsYearCellValidator,
    "is_float_or_not_supplied": IsFloatOrNotSuppliedCellValidator,
    "is_int": IsIntCellValidator,
    "is_uuid": IsUUIDCellValidator,
}
