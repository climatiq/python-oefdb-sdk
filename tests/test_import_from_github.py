def test_import_from_github() -> None:
    import oefdb

    oefdb.import_from_github(repo_reference="motin/Open-Emission-Factors-DB")
    oefdb.import_from_github(pr=1, repo_reference="motin/Open-Emission-Factors-DB")

    assert (
        "Empty assert to ensure pytest passes as long as the above commands succeeds."
    )
