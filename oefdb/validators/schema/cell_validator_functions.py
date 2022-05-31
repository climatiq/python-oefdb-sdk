from __future__ import annotations

import re
import typing
import uuid
from datetime import datetime

from oefdb.validators.schema.cell_validators import cell_validator_return_type


def no_fix_available(cell_value: str) -> None:
    """No-op function when no fixing function is available."""
    return None


def has_no_commas(cell_value: typing.Any) -> cell_validator_return_type:
    """Ensure that the given cell is a non-empty string and contains no commas."""
    if isinstance(cell_value, str):
        if "," in cell_value:
            return f"String '{cell_value}' contains commas. Those are not allowed."

        return None

    return f"'{cell_value}' was not a valid string"


valid_id_punctuation_regex = re.compile(r"-|_|\.")


def is_legal_id(cell_value: str) -> cell_validator_return_type:
    # If we have an alphanumeric string after removing all valid punctuation, then our ID is legal
    value_without_punctuation = re.sub(valid_id_punctuation_regex, "", cell_value)
    if not value_without_punctuation.isalnum():
        return 'Cell contains invalid punctuation. IDs can only contain alphanumeric characters and "-", "_" and "."'

    return None


def is_ascii(cell_value: typing.Any) -> cell_validator_return_type:
    """Ensure that the given cell only contains ASCII characters."""
    if isinstance(cell_value, str):
        if cell_value.isascii():
            return None

        # Try to get a better error message in regards to what string broke
        for (index, char) in enumerate(cell_value):
            if 0 <= ord(char) <= 127:
                pass
            else:
                return f"String '{cell_value}' contains disallowed non-ASCII characters. First invalid character is '{char}' at index {index}."

        # If we for some reason can't detect the character - fallback to this error message.
        return f"String '{cell_value}' contains non-ASCII characters. Those are not allowed."

    return f"'{cell_value}' was not a valid string"


def is_year(cell_value: str) -> cell_validator_return_type:
    """
    Ensure that a given cell is a valid year.

    Currently, it checks that it is between 1980 and 2030
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
    """Ensure that a cell is a float, or the string "not-supplied"."""
    if cell_value == "not-supplied":
        return None

    try:
        float(cell_value)
        return None
    except ValueError:
        pass
    return f"'{cell_value}' was not a valid float or the string 'not-supplied'"


def is_int(cell_value: str) -> cell_validator_return_type:
    """Ensure that a given cell can be converted to an int."""
    try:
        int(cell_value)
        return None

    except ValueError:
        return f"'{cell_value}' was not a valid integer"


def is_date(cell_value: str) -> cell_validator_return_type:
    """Ensure that a given cell can be converted to a date of the format YYYY-MM-DD."""
    try:
        datetime.strptime(cell_value, "%Y/%m/%d")
        return None
    except ValueError:
        return f"'{cell_value}' was not able to be parsed as a date. The format must be YYYY/MM/DD, so e.g. 2020/01/22"


def is_link(cell_value: str) -> cell_validator_return_type:
    """Ensure that a given cell is a link."""
    try:
        if cell_value.startswith("http"):
            return None
        else:
            return f"Link '{cell_value}' does not start with 'http'"
    except AttributeError:
        return f"Unable to parse '{cell_value}' as a string."


def validate_is_uuid(cell_value: str) -> cell_validator_return_type:
    """Ensure that a given cell is a version 4 UUID."""
    if not is_uuid(cell_value):
        return f"'{cell_value}' was not a valid version 4 UUID"

    return None


def is_uuid(val: typing.Any) -> bool:
    try:
        uuid.UUID(val, version=4)
        return True
    except ValueError:
        return False


def generate_uuid(cell_value: str) -> typing.Union[str, None]:
    """Generate a v4 UUID."""
    return str(uuid.uuid4())
