import toml

from oefdb.validators.schema.column_schema import ColumnSchema
from oefdb.validators.schema.schema import Schema


def schema():
    toml_conf = """
        [[columns]]
        name = "hello"
        validators = []
        allow_empty = true

        [[columns]]
        name = "world"
        validators = []
        allow_empty = true
        """

    conf = toml.loads(toml_conf)

    columns = [ColumnSchema(**conf) for conf in conf["columns"]]
    schema = Schema(columns=columns)

    return schema


def test_header_validation_returns_ok_with_identical_schema():
    headers = ["hello", "world"]

    errors = schema().validate_headers(headers)
    assert not errors


def test_header_validation_returns_error_with_too_many_headers():
    headers = ["hello", "world", "wow"]

    errors = schema().validate_headers(headers)

    assert (
        errors[0]
        == "Got more columns than expected. Please delete the extra columns or configure your schema file with the extra columns.: ['wow']"
    )


def test_header_validation_returns_error_with_too_few_headers():
    headers = ["hello"]

    errors = schema().validate_headers(headers)

    assert errors[0] == "Expected column 2 to be 'world', but found no column"
