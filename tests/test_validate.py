from click.testing import CliRunner

from tests.utils import load_oefdb_fixture


def test_validate() -> None:
    import oefdb

    valid_oefdb_df = load_oefdb_fixture("valid_oefdb_df")

    validation_result, results_from_validators = oefdb.validate(valid_oefdb_df)

    assert validation_result is True


def test_validate_cli():
    from oefdb.validate import cli

    runner = CliRunner()
    from os.path import join

    from tests.utils import fixtures_dir_path

    result = runner.invoke(cli, ["-i", join(fixtures_dir_path, "valid_oefdb_df.csv")])
    assert result.exit_code == 0
