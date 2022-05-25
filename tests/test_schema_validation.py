from os.path import join

from click.testing import CliRunner

from oefdb.validate_schema import validate_schema_cli_command
from tests.utils import fixtures_dir_path


def test_validate_schema_cli():
    runner = CliRunner()

    csv_path = join(fixtures_dir_path, "valid_oefdb_df.csv")
    schema_path = join(fixtures_dir_path, "schemas", "valid_schema.toml")

    result = runner.invoke(
        validate_schema_cli_command,
        ["-i", csv_path, "-s", schema_path],
    )

    print("result", result)



    if result.exit_code != 0:
        print(result.output)  # noqa: T001,T201

    assert result.exit_code == 0
