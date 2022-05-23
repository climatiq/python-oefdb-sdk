import csv
import datetime
import math
import pprint
import typing
from typing import List, Optional

import toml
from pydantic import BaseModel

from oefdb.new.configuration import (
    ColumnConfiguration,
    ColumnSchema,
    load_schema_definition,
)


def schema():
    toml_conf = """
        [[columns]]
        name = "hello"
        validators = ["is_float_or_not_supplied"]
        allow_empty = true

        [[columns]]
        name = "world"
        validators = ["is_year"]
        allow_empty = true
        """

    conf = toml.loads(toml_conf)

    columns = [ColumnConfiguration(**conf) for conf in conf["columns"]]
    schema = ColumnSchema(columns=columns)

    return schema


def test_validation_of_csv_files_will_return_ok_on_valid():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
    ]

    (valid, errors) = schema().validate_all(csv)
    print(valid, errors)
    pprint.pp(errors)

    assert valid is True
    assert errors == {}


def test_validation_of_csv_files():
    csv = [
        ["hello", "world"],
        ["1", "not_a_year"],
    ]

    (valid, errors) = schema().validate_all(csv)
    print(valid, errors)
    pprint.pp(errors)

    assert valid is False
    assert errors == {
        1: {"world": {"is_year": ["'not_a_year' was not a valid number"]}}
    }


def test_validation_of_year():
    config = ColumnConfiguration(
        name="config", validators=["is_year"], allow_empty=False
    )

    valid, errors = config.validate_cell("2013")
    assert valid is True
    assert errors == {}


def test_validation_of_wrong_year():
    config = ColumnConfiguration(
        name="config", validators=["is_year"], allow_empty=False
    )

    valid, errors = config.validate_cell("noo")

    pprint.pp(errors)

    assert valid is False
    assert errors == {"is_year": ["'noo' was not a valid number"]}


def test_validation_of_larger_csv_files():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
        ["1.32", "not_a_year"],
        ["1.99", "2021"],
        ["not_float", "2021"],
    ]

    (valid, errors) = schema().validate_all(csv)
    print(valid, errors)
    pprint.pp(errors)

    assert valid is False
    assert errors == {
        2: {"world": {"is_year": ["'not_a_year' was not a valid number"]}},
        4: {
            "hello": {
                "is_float_or_not_supplied": [
                    "'not_float' was not a valid float " "or the string 'not-supplied'"
                ]
            }
        },
    }
