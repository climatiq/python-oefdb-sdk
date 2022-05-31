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


def test_fixing_of_strings_without_comma():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
    ]

    validation_result = schema_fixture().validate_all(csv)

    assert validation_result.is_valid() is True

