from oefdb.validators.schema.column_schema import ColumnSchema


def test_validation_of_year_returns_none():
    config = ColumnSchema(name="config", validators=["is_year"], allow_empty=False)

    validation_error = config.validate_cell("2013")
    assert validation_error is None


def test_validation_of_wrong_year_returns_error():
    config = ColumnSchema(name="config", validators=["is_year"], allow_empty=False)

    validation_error = config.validate_cell("noo")

    assert validation_error == {"is_year": "'noo' was not a valid number"}


def test_validation_of_float_accepts_empty_values_if_allow_empty_set_to_true():
    config = ColumnSchema(
        name="config", validators=["is_float_or_not_supplied"], allow_empty=True
    )

    validation_error = config.validate_cell("")

    assert validation_error is None


def test_validation_of_float_rejects_empty_values_if_allow_empty_set_to_false():
    config = ColumnSchema(
        name="config", validators=["is_float_or_not_supplied"], allow_empty=False
    )

    validation_error = config.validate_cell("")

    assert validation_error == {
        "is_float_or_not_supplied": "'' was not a valid float or the string 'not-supplied'"
    }


def test_no_commas_rejects_strings_with_comma():
    config = ColumnSchema(
        name="config", validators=["has_no_commas"], allow_empty=False
    )

    validation_error = config.validate_cell("hello,")

    assert validation_error == {
        "has_no_commas": "String 'hello,' contains commas. Those are not allowed."
    }


def test_has_no_commas_accepts_non_ascii_string():
    config = ColumnSchema(
        name="config", validators=["has_no_commas"], allow_empty=False
    )

    validation_error = config.validate_cell("æøå")

    assert validation_error is None


def test_is_ascii_rejects_non_ascii_string():
    config = ColumnSchema(name="config", validators=["is_ascii"], allow_empty=False)

    validation_error = config.validate_cell("æøå")

    assert validation_error == {
        "is_ascii": "String 'æøå' contains disallowed non-ASCII characters. First invalid character is 'æ' at index 0."
    }

def test_is_legal_id_rejects_punctuation():
    config = ColumnSchema(name="config", validators=["is_legal_id"], allow_empty=False)

    validation_error = config.validate_cell("hello!")

    assert validation_error == {
        "is_legal_id": 'Cell contains invalid punctuation. IDs can only contain alphanumeric characters and "-", "_" and "."'
    }
