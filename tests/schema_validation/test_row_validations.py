import pprint

import toml

from oefdb.schema_validation.column_schema import ColumnSchema
from oefdb.schema_validation.schema import Schema


def schema_fixture():
    toml_conf = """
        [[columns]]
        name = "hello"
        validators = ["is_float_or_not_supplied"]
        allow_empty = false

        [[columns]]
        name = "world"
        validators = ["is_year"]
        allow_empty = true
        """

    conf = toml.loads(toml_conf)

    columns = [ColumnSchema(**conf) for conf in conf["columns"]]
    schema = Schema(columns=columns)

    return schema


def test_validation_of_csv_files_will_return_ok_on_valid():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
    ]

    (valid, errors) = schema_fixture().validate_all(csv)
    print(valid, errors)
    pprint.pp(errors)

    assert valid is True
    assert errors == {}


def test_validation_of_csv_files():
    csv = [
        ["hello", "world"],
        ["1", "not_a_year"],
    ]

    (valid, errors) = schema_fixture().validate_all(csv)
    print(valid, errors)
    pprint.pp(errors)

    assert valid is False
    assert errors == {
        1: {"world": {"is_year": ["'not_a_year' was not a valid number"]}}
    }


def test_validation_of_year():
    config = ColumnSchema(
        name="config", validators=["is_year"], allow_empty=False
    )

    valid, errors = config.validate_cell("2013")
    assert valid is True
    assert errors == {}


def test_validation_of_wrong_year():
    config = ColumnSchema(
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

    (valid, errors) = schema_fixture().validate_all(csv)
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


def test_validation_is_empty_accepts_empty_values_if_set_to_true():
    csv = [
        ["hello", "world"],
        ["1.32", ""],
    ]

    toml_schema = schema_fixture()
    print(toml_schema)

    (valid, errors) = toml_schema.validate_all(csv)
    print(valid, errors)
    pprint.pp(errors)

    assert valid is True
    assert errors == {}


def test_validation_is_empty_rejects_empty_values_if_set_to_false():
    csv = [
        ["hello", "world"],
        ["", "2013"],
    ]

    toml_schema = schema_fixture()
    print(toml_schema)

    (valid, errors) = toml_schema.validate_all(csv)
    print(valid, errors)
    pprint.pp(errors)

    assert valid is False
    assert errors == {
        2: {
            "hello": {
                "is_float_or_not_supplied": [
                    "'' was not a valid float or the " "string 'not-supplied'"
                ]
            }
        },
    }
