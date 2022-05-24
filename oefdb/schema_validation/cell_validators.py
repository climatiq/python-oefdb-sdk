import math
import typing
from datetime import datetime

from oefdb.validators._typing import validator_result_type


def is_string(cell_value: str) -> validator_result_type:
    # TODO should also check for commas
    if isinstance(cell_value, str):
        if "," in cell_value:
            return False, [
                f"String '{cell_value}' contains commas. Those are not allowed."
            ]

        if cell_value == "":
            return False, ["Cell is empty"]
        else:
            return True, []
    return False, [f"'{cell_value}' was not a valid string"]


def is_year(cell_value: str) -> validator_result_type:
    try:
        year = float(cell_value)
    except ValueError:
        return False, [f"'{cell_value}' was not a valid number"]

    if 1970 < year < 2030:
        return True, []
    return False, [f"'{cell_value}' was not a valid year"]


def is_float_or_not_supplied(cell_value: str) -> validator_result_type:
    if cell_value == "not-supplied":
        return True, []

    try:
        float(cell_value)
        return True, []
    except ValueError:
        pass
    return False, [f"'{cell_value}' was not a valid float or the string 'not-supplied'"]


def is_int(cell_value: str) -> validator_result_type:
    try:
        int(cell_value)
        return True, []

    except ValueError:
        return False, [f"'{cell_value}' was not a valid integer"]


def is_date(cell_value: str) -> validator_result_type:
    try:
        time = datetime.strptime(cell_value, "%Y/%m/%d")
        return True, []
    except ValueError:
        return False, [
            f"'{cell_value}' was not able to be parsed as a date. The format must be YYYY/MM/DD, so e.g. 2020/01/22"
        ]


def is_link(cell_value: str) -> validator_result_type:
    try:
        if cell_value.startswith("http"):
            return True, []
        else:
            return False, [f"Link '{cell_value}' does not start with 'http'"]
    except AttributeError:
        return False, [f"Unable to parse '{cell_value}' as a string."]


ALL_VALIDATORS = {
    "is_string": is_string,
    "is_date": is_date,
    "is_link": is_link,
    "is_year": is_year,
    "is_float_or_not_supplied": is_float_or_not_supplied,
    "is_int": is_int,
}
