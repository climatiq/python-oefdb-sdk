from click.testing import CliRunner


def test_import_from_github() -> None:
    import oefdb

    oefdb.import_from_github(repo_reference="climatiq/Open-Emission-Factors-DB-Dev")
    oefdb.import_from_github(
        pr=1, repo_reference="climatiq/Open-Emission-Factors-DB-Dev"
    )

    assert (
        "Empty assert to ensure pytest passes as long as the above commands succeeds."
    )


def test_import_from_github_cli():
    from oefdb.import_from_github import cli

    runner = CliRunner()
    from tempfile import NamedTemporaryFile

    output_file = NamedTemporaryFile()
    result = runner.invoke(cli, ["-o", output_file.name])
    assert result.exit_code == 0
