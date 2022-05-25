from typing import Dict, List

from pydantic import BaseModel

""" Dict of {rowNumber: {column_name: {validator_name: error}}} """
RowErrorsType = Dict[int, Dict[str, Dict[str, str]]]


class SchemaValidationResult(BaseModel):
    """Dict of {rowNumber: {column_name: {validator_name: error}}}"""

    # Row number -> Column(s) -> Validator_name -> Error
    """
    rowNumber (int): {
        column_name (string): {
            validator_name (string): {
                error: string
            }
        }
    }

    """

    row_errors: RowErrorsType
    column_errors: List[str]

    def valid(self):
        return not bool(self.row_errors) and not bool(self.column_errors)

    def __bool__(self):
        return self.valid()
