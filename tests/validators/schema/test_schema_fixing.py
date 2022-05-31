import pprint

from oefdb.validators.schema.cell_validator_functions import is_uuid
from oefdb.validators.schema.cell_validators import CellValidator, IsUUIDCellValidator
from oefdb.validators.schema.column_schema import ColumnSchema
from oefdb.validators.schema.schema import Schema

add_2_validator = CellValidator(
    validator_name="add_2_to_int",
    validator_function=lambda x: "some error",
    fixer_function=lambda x: int(x) + 2,
)

postfix_dots_validator = CellValidator(
    validator_name="add_2_to_int",
    validator_function=lambda x: "some error",
    fixer_function=lambda x: x + "...",
)


def test_fixing_infrastructure_returns_updated_rows():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
    ]

    schema = Schema(
        columns=[
            ColumnSchema(name="hello", validators=[add_2_validator], allow_empty=True),
            ColumnSchema(name="world", validators=[], allow_empty=True),
        ]
    )

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

    schema = Schema(
        columns=[
            ColumnSchema(name="hello", validators=[add_2_validator], allow_empty=True),
            ColumnSchema(name="world", validators=[], allow_empty=True),
        ]
    )

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

    schema = Schema(
        columns=[
            ColumnSchema(
                name="hello", validators=[postfix_dots_validator], allow_empty=False
            ),
            ColumnSchema(
                name="world", validators=[postfix_dots_validator], allow_empty=True
            ),
        ]
    )

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


def test_fixing_only_attempts_fix_if_validation_of_row_fails():
    csv = [
        ["hello", "world"],
        ["1", "2013"],
        ["", "2013"],
    ]

    # This has a fixer, but it returns no error in validation
    always_validating_validator = CellValidator(
        validator_name="add_2_to_int",
        validator_function=lambda x: None,
        fixer_function=lambda x: x + "!",
    )

    schema = Schema(
        columns=[
            ColumnSchema(
                name="hello", validators=[always_validating_validator], allow_empty=True
            ),
            ColumnSchema(
                name="world", validators=[always_validating_validator], allow_empty=True
            ),
        ]
    )

    fix_result = schema.fix_all(csv)

    print("changed")
    pprint.pp(fix_result.changed_rows)
    print("new values")
    pprint.pp(fix_result.rows_with_fixed_values)

    assert fix_result.changes_applied() is False
    assert fix_result.changed_rows == []
    assert fix_result.rows_with_fixes() == [
        ["hello", "world"],
        ["1", "2013"],
        ["", "2013"],
    ]


def test_can_generate_uuid_if_none_exists():
    csv = [
        ["id", "world"],
        ["dce9092b-85b7-4b6b-bffb-faa77c4191e6", "2013"],
        ["", "2013"],
        ["not_an_id", "2013"],
    ]

    schema = Schema(
        columns=[
            ColumnSchema(
                name="hello", validators=[IsUUIDCellValidator], allow_empty=False
            ),
            ColumnSchema(name="world", validators=[], allow_empty=True),
        ]
    )

    fix_result = schema.fix_all(csv)

    print("changed")
    pprint.pp(fix_result.changed_rows)
    print("new values")
    pprint.pp(fix_result.rows_with_fixed_values)

    assert fix_result.changes_applied() is True
    assert fix_result.changed_rows == [3, 4]

    rows_with_fixes = fix_result.rows_with_fixes()

    assert rows_with_fixes[1] == ["dce9092b-85b7-4b6b-bffb-faa77c4191e6", "2013"]
    assert is_uuid(rows_with_fixes[2][0])
    assert is_uuid(rows_with_fixes[3][0])
