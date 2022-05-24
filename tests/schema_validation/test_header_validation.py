import toml

from oefdb.schema_validation.configuration import ColumnConfiguration, ColumnSchema


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

    columns = [ColumnConfiguration(**conf) for conf in conf["columns"]]
    schema = ColumnSchema(columns=columns)

    return schema


def test_header_validation_returns_ok_with_identical_schema():
    headers = ["hello", "world"]

    (valid, errors) = schema().validate_headers(headers)
    assert valid is True


def test_header_validation_returns_error_with_too_many_headers():
    headers = ["hello", "world", "wow"]

    (valid, errors) = schema().validate_headers(headers)

    print(valid, errors)
    assert (
        errors[0]
        == "Got more columns than expected. Please delete the extra columns or configure your schema file with the extra columns.: ['wow']"
    )
    assert valid is False


def test_header_validation_returns_error_with_too_few_headers():
    headers = ["hello"]

    (valid, errors) = schema().validate_headers(headers)

    print(valid, errors)
    assert errors[0] == "Expected column 1 to be 'world', but found no column"
    assert valid is False
