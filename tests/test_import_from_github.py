def test_import_from_github() -> None:
    import oefdb

    oefdb.import_from_github()
    oefdb.import_from_github(pr=83)

    assert (
        "Empty assert to ensure pytest passes as long as the above commands succeeds."
    )
