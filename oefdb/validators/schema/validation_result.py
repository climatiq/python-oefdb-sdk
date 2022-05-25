from typing import Dict, List

from pydantic import BaseModel

""" Dict of {rowNumber: {column_name: {validator_name: error}}} """
RowErrorsType = Dict[int, Dict[str, Dict[str, str]]]


class SchemaValidationResult(BaseModel):
    """Errors encountered while validating rows"""
    row_errors: RowErrorsType
    """Errors encountered while validating column structure"""
    column_errors: List[str]

    """Is the thing being validated valid? Returns true if there are no errors."""
    def valid(self):
        return not bool(self.row_errors) and not bool(self.column_errors)