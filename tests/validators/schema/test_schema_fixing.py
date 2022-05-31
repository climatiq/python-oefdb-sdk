import pprint

from oefdb.validators.schema.cell_validators import CellValidator
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


add_2_validator = CellValidator(validator_name="add_2_to_int", validator_function=lambda x: None,
                                fixer_function=lambda x: int(x) + 2)

postfix_dots_validator = CellValidator(validator_name="add_2_to_int", validator_function=lambda x: None,
                                fixer_function=lambda x: x + "...")


def test_fixing_infrastructure_returns_updated_rows():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
    ]

    schema = Schema(columns=[
        ColumnSchema(
            name="hello",
            validators=[add_2_validator],
            allow_empty=True
        ),
        ColumnSchema(
            name="world",
            validators=[],
            allow_empty=True
        )
    ])

    fix_result = schema.fix_all(csv)

    pprint.pp(fix_result.changed_rows)
    pprint.pp(fix_result.rows_with_fixed_values)

    assert fix_result.changes_applied() is True
    assert fix_result.changed_rows == [2]
    assert fix_result.rows_with_fixes() == [
        ["hello", "world"],
        ["3", "2013"],
    ]


def test_fixing_does_not_fix_empty_values_if_allow_empty_true():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
        ["", "2013"],
    ]

    schema = Schema(columns=[
        ColumnSchema(
            name="hello",
            validators=[add_2_validator],
            allow_empty=True
        ),
        ColumnSchema(
            name="world",
            validators=[],
            allow_empty=True
        )
    ])

    fix_result = schema.fix_all(csv)

    pprint.pp(fix_result.changed_rows)
    pprint.pp(fix_result.rows_with_fixed_values)

    assert fix_result.changes_applied() is True
    assert fix_result.changed_rows == [2]
    assert fix_result.rows_with_fixes() == [
        ["hello", "world"],
        ["3", "2013"],
        ["", "2013"],
    ]


def test_fixing_attempts_to_fix_empty_values_if_allow_empty_false():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
        ["", "2013"],
    ]

    schema = Schema(columns=[
        ColumnSchema(
            name="hello",
            validators=[postfix_dots_validator],
            allow_empty=False
        ),
        ColumnSchema(
            name="world",
            validators=[postfix_dots_validator],
            allow_empty=True
        )
    ])

    fix_result = schema.fix_all(csv)

    pprint.pp(fix_result.changed_rows)
    pprint.pp(fix_result.rows_with_fixed_values)

    assert fix_result.changes_applied() is True
    assert fix_result.changed_rows == [2, 3]
    assert fix_result.rows_with_fixes() == [
        ["hello", "world"],
        ["1...", "2013..."],
        ["...", "2013..."],
    ]


# Todo remove
def test_fixing_performs_schema_validation_first():
    csv = [
        ["WrOnG"],
        ["1",],
        ["",],
    ]

    schema = Schema(columns=[
        ColumnSchema(
            name="hello",
            validators=[postfix_dots_validator],
            allow_empty=False
        ),
        ColumnSchema(
            name="world",
            validators=[postfix_dots_validator],
            allow_empty=True
        )
    ])

    fix_result = schema.fix_all(csv)

    pprint.pp(fix_result)

    raise Exception("sfsd")
