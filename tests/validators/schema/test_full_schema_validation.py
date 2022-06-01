from oefdb.validators.schema.cell_validators import IsValidActivityIdCellValidator, IsAsciiCellValidator
from oefdb.validators.schema.column_schema import ColumnSchema
from oefdb.validators.schema.schema import Schema


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

    return Schema.from_toml_string(toml_conf)


def test_validation_of_csv_files_will_return_ok_on_valid():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
    ]

    validation_result = schema_fixture().validate_all(csv)

    assert validation_result.is_valid() is True


def test_validation_of_csv_files():
    csv = [
        ["hello", "world"],
        ["1", "not_a_year"],
    ]

    validation_result = schema_fixture().validate_all(csv)

    assert validation_result.is_valid() is False
    assert not validation_result.column_errors
    assert validation_result.row_errors == {
        2: {"world": {"is_year": "'not_a_year' was not a valid number"}}
    }


def test_validation_of_csv_files_with_multiple_errors_on_same_row():
    csv = [
        ["hello", "world"],
        ["a_string", "not_a_year"],
    ]

    validation_result = schema_fixture().validate_all(csv)

    assert validation_result.is_valid() is False
    assert not validation_result.column_errors
    assert validation_result.row_errors == {
        2: {
            "hello": {
                "is_float_or_not_supplied": "'a_string' was not a valid float or the string 'not-supplied'"
            },
            "world": {"is_year": "'not_a_year' was not a valid number"},
        }
    }


def test_validation_of_csv_files_with_multiple_errors_on_same_cell():
    toml_conf = """
            [[columns]]
            name = "hello"
            validators = ["has_no_commas", "is_link"]
            allow_empty = false
            """

    schema = Schema.from_toml_string(toml_conf)

    csv = [
        ["hello"],
        [","],
    ]

    validation_result = schema.validate_all(csv)

    assert validation_result.is_valid() is False
    assert not validation_result.column_errors
    assert validation_result.row_errors == {
        2: {
            "hello": {
                "has_no_commas": "String ',' contains commas. Those are not allowed.",
                "is_link": "Link ',' does not start with 'http'",
            }
        }
    }


def test_validation_of_larger_csv_files():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
        ["1.32", "not_a_year"],
        ["1.99", "2021"],
        ["not_float", "2021"],
    ]

    validation_result = schema_fixture().validate_all(csv)

    assert validation_result.is_valid() is False
    assert not validation_result.column_errors
    assert validation_result.row_errors == {
        3: {"world": {"is_year": "'not_a_year' was not a valid number"}},
        5: {
            "hello": {
                "is_float_or_not_supplied": "'not_float' was not a valid float or the string 'not-supplied'"
            }
        },
    }


def test_validation_is_empty_accepts_empty_values_if_set_to_true():
    csv = [
        ["hello", "world"],
        ["1.32", ""],
    ]

    toml_schema = schema_fixture()

    validation_result = toml_schema.validate_all(csv)
    assert validation_result.is_valid() is True
    assert not validation_result.row_errors
    assert not validation_result.column_errors


def test_validation_is_empty_rejects_empty_values_if_set_to_false():
    csv = [
        ["hello", "world"],
        ["", "2013"],
    ]

    toml_schema = schema_fixture()

    validation_result = toml_schema.validate_all(csv)

    assert validation_result.is_valid() is False
    assert not validation_result.column_errors

    assert validation_result.row_errors == {
        2: {
            "hello": {
                "allow_empty": "The cell was empty, but empty cells are not allowed."
            }
        },
    }


def test_validation_rejects_values_not_in_allowed_values():
    csv = [
        ["hello", "world"],
        ["", "2013"],
    ]

    schema = Schema(
        columns=[
            ColumnSchema(
                name="hello", validators=[], allow_empty=True
            ),
            ColumnSchema(
                name="world", validators=[], allow_empty=True, allowed_values=["2014"]
            ),
        ]
    )

    validation_result = schema.validate_all(csv)

    assert validation_result.is_valid() is False
    assert not validation_result.column_errors

    assert validation_result.row_errors == {
        2: {
            "world": {
                "allowed_values": "The value '2013' was not part of the 'allowed_values' list. Please edit the cell or the list of allowed values."
            }
        },
    }

def test_validation_does_not_reject_empty_values_if_allow_empty_is_set_to_true_even_if_value_is_not_in_allowed_values():
    csv = [
        ["hello", "world"],
        ["", ""],
    ]

    schema = Schema(
        columns=[
            ColumnSchema(
                name="hello", validators=[], allow_empty=True
            ),
            ColumnSchema(
                name="world", validators=[], allow_empty=True, allowed_values=["2014"]
            ),
        ]
    )

    validation_result = schema.validate_all(csv)

    assert validation_result.is_valid() is True


def test_validation_still_fails_on_elements_in_allowed_values_if_validator_fails():
    csv = [
        ["hello", "world"],
        ["", "æøå"],
    ]

    schema = Schema(
        columns=[
            ColumnSchema(
                name="hello", validators=[], allow_empty=True
            ),
            ColumnSchema(
                name="world", validators=[IsAsciiCellValidator], allow_empty=True, allowed_values=["æøå"]
            ),
        ]
    )

    validation_result = schema.validate_all(csv)

    assert validation_result.is_valid() is False
    assert not validation_result.column_errors

    assert validation_result.row_errors == {
        2: {
            "world": {
                "is_ascii": "String 'æøå' contains disallowed non-ASCII characters. First invalid character is 'æ' at index 0."
            }
        },
    }
