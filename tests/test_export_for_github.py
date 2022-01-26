from click.testing import CliRunner
from pandas import DataFrame


def test_export_for_github() -> None:

    import oefdb

    oefdb_df = DataFrame()
    oefdb.export_for_github(oefdb_df)

    from tempfile import NamedTemporaryFile

    f = NamedTemporaryFile()
    oefdb.export_for_github(oefdb_df, export_path=f.name)

    assert (
        "Empty assert to ensure pytest passes as long as the above commands succeeds."
    )


def test_export_for_github_cli():
    from oefdb.export_for_github import cli

    runner = CliRunner()
    from tempfile import NamedTemporaryFile

    output_file = NamedTemporaryFile()
    from os.path import join

    from tests.utils import fixtures_dir_path

    result = runner.invoke(
        cli,
        ["-i", join(fixtures_dir_path, "valid_oefdb_df.csv"), "-o", output_file.name],
    )
    assert result.exit_code == 0
