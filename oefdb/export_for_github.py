from typing import Optional

from pandas import DataFrame


def export_for_github(oefdb_df: DataFrame, export_path: Optional[str] = None) -> None:
    import oefdb

    oefdb_csv = oefdb.to_oefdb_csv(oefdb_df)

    if export_path:
        export_for_github_via_save_file(oefdb_csv, export_path)

    from IPython import get_ipython

    ipy = get_ipython()
    if ipy:
        export_for_github_via_notebook_textarea_copy_paste(oefdb_csv)
    else:
        import pyperclip

        try:
            export_for_github_via_copy_to_clipboard(oefdb_csv)
        except pyperclip.PyperclipException:
            export_for_github_via_save_file(oefdb_csv, "OpenEmissionFactorsDB.csv")


def export_for_github_via_save_file(oefdb_csv: str, export_path: str) -> None:
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