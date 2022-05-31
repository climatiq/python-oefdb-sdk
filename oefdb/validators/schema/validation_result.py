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

    def is_valid(self) -> bool:
        """Check whether the schema was valid. Returns true if there are no errors."""
        return not bool(self.row_errors) and not bool(self.column_errors)


class SchemaFixResult(BaseModel):
    """The result of fixing a schema."""

    # What rows were changed while fixing this schema
    changed_row_indexes: List[int]
    # All rows but with fixed values
    rows_with_fixed_values: CsvRows

    def changes_applied(self) -> bool:
        """Return whether fixing applied any changes."""
        return bool(self.changed_row_indexes)

    def rows_with_fixes(self) -> CsvRows:
        """
        Return all CsvRows with any fixes applied.

        This will return the original rows with no changes if no fixes were applied.
        """
        return self.rows_with_fixed_values
