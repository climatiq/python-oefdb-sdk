from tests.utils import load_oefdb_fixture


def test_validate() -> None:
    import oefdb

    valid_oefdb_df = load_oefdb_fixture("valid_oefdb_df")

    validation_result, results_from_validators = oefdb.validate(valid_oefdb_df)

    assert validation_result is True
