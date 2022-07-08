import csv
import pathlib
import tempfile

from click.testing import CliRunner

from oefdb.format_csv import format_csv_cli_command
from oefdb.validate_schema import validate_schema_cli_command
from oefdb.validators.schema.cell_validator_functions import is_uuid


def test_format_csv_cli():

    with tempfile.NamedTemporaryFile(
        "w+",
    ) as csv_file:
        runner = CliRunner()

        csv_content = 'id,foo\r\n"some string with quotes",123\r\nno quotes, 1234'

        # --- Write CSV file and record original contents for comparison with backup file
        csv_file.write(csv_content)

        # Invoke CLI
        result = runner.invoke(
            format_csv_cli_command,
            ["-i", csv_file.name],
        )

        if result.exit_code != 0:
            print(result.output)

        assert result.exit_code == 0

        # Assert that the written CSV file now has UUIDs in the id column
        csv_file.seek(0)
        csv = csv_file.read()

        print(repr(csv))

        raise "123"
