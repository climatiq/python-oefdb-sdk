from tests.utils import load_oefdb_fixture


def test_check_ids_for_unsupported_characters():
    from oefdb.validators import check_ids_for_unsupported_characters

    oefdb_df_without_invalid_characters_in_the_id_column = load_oefdb_fixture(
        "oefdb_df_without_invalid_characters_in_the_id_column"
    )
    validation_result, validation_messages = check_ids_for_unsupported_characters(
        oefdb_df_without_invalid_characters_in_the_id_column
    )
    assert validation_result is True

    oefdb_df_with_invalid_characters_in_the_id_column = load_oefdb_fixture(
        "oefdb_df_with_invalid_characters_in_the_id_column"
    )
    validation_result, validation_messages = check_ids_for_unsupported_characters(
        oefdb_df_with_invalid_characters_in_the_id_column
    )
    assert validation_result is False
