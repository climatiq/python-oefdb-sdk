def test_export_for_github() -> None:
    from pandas import DataFrame

    import oefdb

    oefdb_df = DataFrame()
    oefdb.export_for_github(oefdb_df)

    from tempfile import NamedTemporaryFile

    f = NamedTemporaryFile()
    oefdb.export_for_github(oefdb_df, export_path=f.name)

    assert (
        "Empty assert to ensure pytest passes as long as the above commands succeeds."
    )
