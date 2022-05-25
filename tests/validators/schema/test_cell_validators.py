from oefdb.validators.schema.column_schema import ColumnSchema


def test_validation_of_year_returns_none():
    config = ColumnSchema(name="config", validators=["is_year"], allow_empty=False)

    validation_result = config.validate_cell("2013")
    assert validation_result is None


def test_validation_of_wrong_year_returns_error():
    config = ColumnSchema(name="config", validators=["is_year"], allow_empty=False)

    validation_result = config.validate_cell("noo")

    assert validation_result == {"is_year": "'noo' was not a valid number"}


def test_validation_of_float_accepts_empty_values_if_allow_empty_set_to_true():
    config = ColumnSchema(name="config", validators=["is_float_or_not_supplied"], allow_empty=True)

    validation_result = config.validate_cell("")

    assert validation_result is None


def test_validation_of_float_rejects_empty_values_if_allow_empty_set_to_false():
    config = ColumnSchema(name="config", validators=["is_float_or_not_supplied"], allow_empty=False)

    validation_result = config.validate_cell("")

    assert validation_result == {'is_float_or_not_supplied': "'' was not a valid float or the string 'not-supplied'"}

