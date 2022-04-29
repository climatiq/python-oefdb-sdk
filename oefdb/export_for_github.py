from __future__ import annotations

import click
from pandas import DataFrame


def export_for_github(oefdb_df: DataFrame, export_path: str | None = None) -> None:
    import oefdb

    validation_result, results_from_validators = oefdb.validate(oefdb_df)
    from oefdb.util.present_results_from_validators import (
        present_results_from_validators,
    )

    present_results_from_validators(validation_result, results_from_validators)

    oefdb_csv = oefdb.to_oefdb_csv(oefdb_df)

    if export_path:
        export_oefdb_csv_to_file(oefdb_csv, export_path)
        return

    from IPython import get_ipython

    ipy = get_ipython()
    if ipy:
        export_for_github_via_notebook_textarea_copy_paste(oefdb_csv)
    else:
        import pyperclip

        try:
            export_for_github_via_copy_to_clipboard(oefdb_csv)
        except pyperclip.PyperclipException:
            export_oefdb_csv_to_file(oefdb_csv, "OpenEmissionFactorsDB.csv")


def export_oefdb_csv_to_file(oefdb_csv: str, export_path: str) -> None:
    with open(export_path, "w") as file:
        file.write(oefdb_csv)
    print(f'OEFDB CSV exported to "{export_path}"')  # noqa: T001


def export_for_github_via_copy_to_clipboard(oefdb_csv: str) -> None:
    import pyperclip

    pyperclip.copy(oefdb_csv)
    print("The OEFDB CSV contents has been copied into the clipboard.")  # noqa: T001


def export_for_github_via_notebook_textarea_copy_paste(oefdb_csv: str) -> None:
    import ipywidgets as widgets
    from IPython.display import display
    from ipywidgets import Layout

    display(
        widgets.Textarea(
            value=oefdb_csv,
            placeholder="",
            layout=Layout(width="100%", height="200px"),
            description="OEFDB CSV:",
            disabled=False,
        )
    )


@click.command()
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True),
    help="OEFDB CSV file to validate",
)
@click.option(
    "--output", "-o", required=True, type=str, help="OEFDB CSV file export path"
)
def cli(input: str, output: str) -> None:
    import oefdb

    oefdb_df = oefdb.from_oefdb_csv(input)
    oefdb.export_for_github(oefdb_df, export_path=output)
