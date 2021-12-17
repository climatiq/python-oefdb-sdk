from test_project import __version__


def test_version():
    from pandas import DataFrame

    import oefdb

    oefdb_df = DataFrame()
    oefdb.export_for_github(oefdb_df)
    assert __version__ == "0.1.0"
