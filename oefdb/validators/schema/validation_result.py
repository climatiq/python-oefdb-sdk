from typing import Dict, List

from pydantic import BaseModel

from oefdb.validators._typing import CsvRows

""" Dict of {rowNumber: {column_name: {validator_name: error}}} """
RowErrorsType = Dict[int, Dict[str, Dict[str, str]]]


class SchemaValidationResult(BaseModel):
    """The result of validating a schema."""

    # Errors encountered while validating column structure
    column_errors: List[str]
    # Errors encountered while validating rows.
    row_errors: RowErrorsType

    """
    Is the thing being validated valid? Returns true if there are no errors.
    """

    def is_valid(self) -> bool:
        return not bool(self.row_errors) and not bool(self.column_errors)


class SchemaFixResult(BaseModel):
    """The result of fixing a schema."""

    # What rows were changed while fixing this schema
    changed_rows: List[int]
    # All rows but with fixed values
    rows_with_fixed_values: CsvRows

    """
    Were any changes applied
    """

    def changes_applied(self) -> bool:
        return bool(self.changed_rows)

    """
    Get rows with fixes
    """

    def rows_with_fixes(self) -> CsvRows:
        return self.rows_with_fixed_values
