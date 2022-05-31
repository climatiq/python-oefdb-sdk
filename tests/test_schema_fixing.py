import csv
import pathlib
import tempfile

from click.testing import CliRunner

from oefdb.validate_schema import validate_schema_cli_command
from oefdb.validators.schema.cell_validator_functions import is_uuid


def test_fix_schema_cli():

    with tempfile.NamedTemporaryFile(
        "w+",
    ) as csv_file, tempfile.NamedTemporaryFile("w+") as schema_file:
        runner = CliRunner()

        # --- Write CSV file and record original contents for comparison with backup file
        writer = csv.writer(csv_file)
        writer.writerows(
            [
                ["id", "foo"],
                ["", ""],
                ["not-valid-id", ""],
                ["34c1ae79-cc9d-4435-b7f3-29fbeb71e742", ""],
            ]
        )

        csv_file.flush()
        csv_file.seek(0)
        original_csv_content = csv_file.read()
        csv_file.seek(0)

        # Write schema file
        schema_file.write(
            """
        [[columns]]
        name = "id"
        validators = ["is_uuid"]
        allow_empty = false

        [[columns]]
        name = "foo"
        validators = []
        allow_empty = true
        """
        )
        schema_file.flush()

        # Invoke CLI
        result = runner.invoke(
            validate_schema_cli_command,
            ["-i", csv_file.name, "-s", schema_file.name, "--fix"],
        )

        if result.exit_code != 0:
            print(result.output)

        assert result.exit_code == 0

        # Assert that the written CSV file now has UUIDs in the id column
        csv_file.seek(0)
        csv_lines = list(csv.reader(csv_file))
        # These two are newly generated
        assert is_uuid(csv_lines[1][0])
        assert is_uuid(csv_lines[2][0])
        # This is the same UUID as before
        assert csv_lines[3][0] == "34c1ae79-cc9d-4435-b7f3-29fbeb71e742"

        # Assert that we've written a backup file, and it contains the same content as the original CSV
        backup_file_path = pathlib.Path(csv_file.name).with_suffix(".bak")
        with open(backup_file_path) as backup:
            contents = backup.read()
            assert contents == original_csv_content
        backup_file_path.unlink()  # Delete the backup file here - it's a "real" file so that isn't done automatically.
