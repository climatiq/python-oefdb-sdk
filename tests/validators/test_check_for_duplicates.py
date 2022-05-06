from tests.utils import load_oefdb_fixture


def test_check_for_duplicates():
    from oefdb.validators import check_for_duplicates

    oefdb_df_without_duplicates = load_oefdb_fixture("oefdb_df_without_duplicates")
    validation_result, validation_messages = check_for_duplicates(
        oefdb_df_without_duplicates
    )
    assert validation_result is True

    oefdb_df_with_a_duplicate_row = load_oefdb_fixture("oefdb_df_with_a_duplicate_row")
    validation_result, validation_messages = check_for_duplicates(
        oefdb_df_with_a_duplicate_row
    )
    assert validation_result is False

    oefdb_df_with_a_duplicate_row = load_oefdb_fixture("oefdb_df_with_a_duplicate_uuid")
    validation_result, validation_messages = check_for_duplicates(
        oefdb_df_with_a_duplicate_row
    )
    assert validation_result is False

    oefdb_df_with_a_compound_key_is_duplicate = load_oefdb_fixture(
        "oefdb_df_with_a_compound_key_is_duplicate"
    )
    validation_result, validation_messages = check_for_duplicates(
        oefdb_df_with_a_compound_key_is_duplicate
    )

    assert validation_result is False

    oefdb_df_with_a_compound_key_is_not_duplicate = load_oefdb_fixture(
        "oefdb_df_with_a_compound_key_not_duplicate"
    )
    validation_result, validation_messages = check_for_duplicates(
        oefdb_df_with_a_compound_key_is_not_duplicate
    )

    assert validation_result is True
