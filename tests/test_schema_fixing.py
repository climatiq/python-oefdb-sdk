import csv
import pathlib
import tempfile
from os.path import join

from click.testing import CliRunner

from oefdb.validate_schema import validate_schema_cli_command
from oefdb.validators.schema.cell_validator_functions import is_uuid
from tests.utils import fixtures_dir_path


def test_fix_schema_cli():
    runner = CliRunner()

    with tempfile.NamedTemporaryFile("w+",) as csv_file, tempfile.NamedTemporaryFile("w+") as schema_file:

        with open("./tmp.csv", "w+", newline='') as tmp:

            writer = csv.writer(csv_file)
            writer.writerows([
                ["id", "foo"],
                ["", ""],
                ["not-valid-id", ""],
                ["34c1ae79-cc9d-4435-b7f3-29fbeb71e742", ""],
            ]
            )

            csv_file.flush()
            # tmp.close()
        csv_file.seek(0)
        original_csv_content = csv_file.read()
        csv_file.seek(0)

        # with open("./tmp.csv", "r", newline='') as tmp:
        print("CSV FILE")
        csv_file.seek(0)
        print(csv_file.read())
        for f in csv_file.read():
            print(f)

        print("----")

        schema_file.write("""
        [[columns]]
        name = "id"
        validators = ["is_uuid"]
        allow_empty = false

        [[columns]]
        name = "foo"
        validators = []
        allow_empty = true
        """)
        schema_file.flush()

        print(csv_file.name)
        print(schema_file.name)

        result = runner.invoke(
            validate_schema_cli_command,
            ["-i", csv_file.name, "-s", schema_file.name, "--fix"],
        )

        print(result.output)

        if result.exit_code != 0:
            print(result.output)

        assert result.exit_code == 0

        csv_file.seek(0)
        print("CSV FILE POST READ")
        print(csv_file.read())
        print("-----")
        csv_file.seek(0)

        csv_lines = list(csv.reader(csv_file))

        # CSV lines
        print(csv_lines[1][0])
        assert is_uuid(csv_lines[1][0])
        assert is_uuid(csv_lines[2][0])
        # Same UUID as before
        assert csv_lines[3][0] == "34c1ae79-cc9d-4435-b7f3-29fbeb71e742"

        # We have a backup file
        backup_file_path = pathlib.Path(csv_file.name).with_suffix(".backup")
        print(backup_file_path)
        with open(backup_file_path, "r") as backup:
            contents = backup.read()
            print(contents)
            assert contents == original_csv_content

        assert 1 == 2
