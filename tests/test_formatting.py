import tempfile

from click.testing import CliRunner

from oefdb.format_csv import format_csv_cli_command


def test_format_csv_cli():

    with tempfile.NamedTemporaryFile(
        "w+",
        newline="",
    ) as csv_file:
        runner = CliRunner()

        csv_content = 'id,foo\r\n"some string with quotes",123\r\nno quotes, 1234'

        # --- Write CSV file and record original contents for comparison with backup file
        csv_file.write(csv_content)
        csv_file.flush()

        # Invoke CLI
        result = runner.invoke(
            format_csv_cli_command,
            ["-i", csv_file.name],
        )

        if result.exit_code != 0:
            print(result.output)

        assert result.exit_code == 0

        with open(csv_file.name, newline="") as f:
            updated_contents = f.read()
            # Contents have been updated with:
            # 1. Newlines changed to \n from \r\n
            # 2. Quoted strings have been unquoted
            # 3. A trailing newline has been added
            assert (
                updated_contents
                == "id,foo\nsome string with quotes,123\nno quotes, 1234\n"
            )
