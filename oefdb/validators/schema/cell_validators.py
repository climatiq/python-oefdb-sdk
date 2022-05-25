from __future__ import annotations

import typing
from datetime import datetime

from pydantic import BaseModel

cell_validator_return_type = typing.Union[str, None]


class CellValidator(BaseModel):
    validator_name: str
    validator_function: typing.Callable[[str], cell_validator_return_type]

    def validate_cell(self, obj) -> cell_validator_return_type:
        """
        Cell validators return None if no error is relevant, or a string with an error message
        if any errors have occurred
        """
        return self.validator_function(obj)


def is_allowed_string(cell_value: typing.Any) -> cell_validator_return_type:
    """
    Checks that the given cell is a non-empty string and contains no commas.
    """
    if isinstance(cell_value, str):
        if "," in cell_value:
            return f"String '{cell_value}' contains commas. Those are not allowed."

        if not cell_value.isascii():
            return f"String '{cell_value}' contains non-ASCII characters. Those are not allowed."


        if cell_value == "":
            return "Cell is empty"
        else:
            return None

    return f"'{cell_value}' was not a valid string"


def is_year(cell_value: str) -> cell_validator_return_type:
    """
    Checks that a given cell value is a valid year. Currently, it checks that it is between 1980 and 2030
    as that seems like a very safe bound.
    """
    try:
        year = float(cell_value)
    except ValueError:
        return f"'{cell_value}' was not a valid number"

    if 1970 < year < 2030:
        return None
    return f"'{cell_value}' was not a valid year"


def is_float_or_not_supplied(cell_value: str) -> cell_validator_return_type:
    """
    Checks that a cell is a float, or the string "not-supplied"
    """
    if cell_value == "not-supplied":
        return None

    try:
        float(cell_value)
        return None
    except ValueError:
        pass
    return f"'{cell_value}' was not a valid float or the string 'not-supplied'"


def is_int(cell_value: str) -> cell_validator_return_type:
    """
    Checks that a given cell can be converted to an int
    """
    try:
        int(cell_value)
        return None

    except ValueError:
        return f"'{cell_value}' was not a valid integer"


def is_date(cell_value: str) -> cell_validator_return_type:
    """
    Checks that a given cell can be converted to a date of the format
    YYYY-MM-DD
    """
    try:
        _time = datetime.strptime(cell_value, "%Y/%m/%d")
        return None
    except ValueError:
        return f"'{cell_value}' was not able to be parsed as a date. The format must be YYYY/MM/DD, so e.g. 2020/01/22"


def is_link(cell_value: str) -> cell_validator_return_type:
    """
    Checks that a given cell is a link or not
    """
    try:
        if cell_value.startswith("http"):
            return
        else:
            return f"Link '{cell_value}' does not start with 'http'"
    except AttributeError:
        return f"Unable to parse '{cell_value}' as a string."


ALL_VALIDATORS = {
    "is_allowed_string": is_allowed_string,
    "is_date": is_date,
    "is_link": is_link,
    "is_year": is_year,
    "is_float_or_not_supplied": is_float_or_not_supplied,
    "is_int": is_int,
}
