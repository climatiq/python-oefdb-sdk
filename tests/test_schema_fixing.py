import tempfile
from os.path import join

from click.testing import CliRunner

from oefdb.validate_schema import validate_schema_cli_command
from tests.utils import fixtures_dir_path



def test_fix_schema_cli():
    runner = CliRunner()

    csv_file = tempfile.NamedTemporaryFile()
    schema_file = tempfile.NamedTemporaryFile()

    csv_file.write()

    print(csv_file.name)
    print(schema_file.name)

    raise Exception("svs")

    csv_path = join(fixtures_dir_path, "valid_oefdb_df.csv")
    schema_path = join(fixtures_dir_path, "schemas", "valid_schema.toml")

    result = runner.invoke(
        validate_schema_cli_command,
        ["-i", csv_path, "-s", schema_path],
    )

    if result.exit_code != 0:
        print(result.output)

    assert result.exit_code == 0
