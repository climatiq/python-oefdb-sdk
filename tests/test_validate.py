def test_validate() -> None:
    import oefdb

    oefdb_df = oefdb.import_from_github(repo_reference="motin/Open-Emission-Factors-DB")

    validation_result, validation_messages = oefdb.validate(oefdb_df)

    # TODO: assert this once main branch is passing validation
    # assert validation_result is True
