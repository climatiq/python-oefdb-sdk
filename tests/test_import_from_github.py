def test_import_from_github() -> None:
    import oefdb

    oefdb.import_from_github(repo_reference="climatiq/Open-Emission-Factors-DB-Dev")
    oefdb.import_from_github(
        pr=1, repo_reference="climatiq/Open-Emission-Factors-DB-Dev"
    )

    assert (
        "Empty assert to ensure pytest passes as long as the above commands succeeds."
    )
