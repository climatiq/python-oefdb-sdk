from pandas import DataFrame


def export_for_github(oefdb_df: DataFrame) -> None:
    import ipywidgets as widgets
    from IPython import get_ipython
    from IPython.display import display
    from ipywidgets import Layout

    import oefdb

    oefdb_csv = oefdb.to_oefdb_csv(oefdb_df)

    ipy = get_ipython()
    if ipy:
        display(
            widgets.Textarea(
                value=oefdb_csv,
                placeholder="",
                layout=Layout(width="100%", height="200px"),
                description="OEFDB CSV:",
                disabled=False,
            )
        )
    else:
        import pyperclip

        pyperclip.copy(oefdb_csv)
        print(  # noqa: T001
            "The OEFDB CSV contents has been copied into the clipboard."
        )
