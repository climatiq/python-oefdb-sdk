from tests.utils import load_oefdb_fixture


def test_check_for_empty_uuids():
    from oefdb.validators import check_for_empty_uuids

    oefdb_df_without_duplicates = load_oefdb_fixture("oefdb_df_without_empty_uuids")
    validation_result, validation_messages = check_for_empty_uuids(
        oefdb_df_without_duplicates
    )
    assert validation_result is True

    oefdb_df_with_a_duplicate_row = load_oefdb_fixture("oefdb_df_with_an_empty_uuid")
    validation_result, validation_messages = check_for_empty_uuids(
        oefdb_df_with_a_duplicate_row
    )
    assert validation_result is False
    # TODO: Run create_uuids and validate again, asserting True

    oefdb_df_with_a_duplicate_row = load_oefdb_fixture("oefdb_df_with_many_empty_uuids")
    validation_result, validation_messages = check_for_empty_uuids(
        oefdb_df_with_a_duplicate_row
    )
    assert validation_result is False
    # TODO: Run create_uuids and validate again, asserting True
