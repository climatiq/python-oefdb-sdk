from tests.utils import load_oefdb_fixture


def test_check_oefdb_structure():
    from oefdb.validators import check_oefdb_structure

    oefdb_df_with_a_valid_structure = load_oefdb_fixture(
        "oefdb_df_with_a_valid_structure"
    )
    validation_result, validation_messages = check_oefdb_structure(
        oefdb_df_with_a_valid_structure
    )
    assert validation_result is True

    oefdb_df_with_a_column_missing = load_oefdb_fixture(
        "oefdb_df_with_a_column_missing"
    )
    validation_result, validation_messages = check_oefdb_structure(
        oefdb_df_with_a_column_missing
    )
    assert validation_result is False

    oefdb_df_with_an_extra_column = load_oefdb_fixture("oefdb_df_with_an_extra_column")
    validation_result, validation_messages = check_oefdb_structure(
        oefdb_df_with_an_extra_column
    )
    assert validation_result is False

    oefdb_df_with_a_misnamed_column = load_oefdb_fixture(
        "oefdb_df_with_a_misnamed_column"
    )
    validation_result, validation_messages = check_oefdb_structure(
        oefdb_df_with_a_misnamed_column
    )
    assert validation_result is False
