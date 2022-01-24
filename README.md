# Open Emission Factors Database SDK for Python

Tools for interacting with and contributing to the [Open Emission Factors DB](https://github.com/climatiq/Open-Emission-Factors-DB).

## Installation

Using pip:

```shell
pip install oefdb
```

Using [Poetry](https://python-poetry.org/):

```shell
poetry add oefdb
```

## Usage

Import the library:

```py
import oefdb
```

### Importing the existing OEFDB data

Import the latest version from GitHub as a Pandas dataframe:

```py
oefdb_df = oefdb.import_from_github()
```

### Contributing your OEFDB data changes/improvements

After making suggested changes to the imported dataframe, you can contribute these changes to OEFDB as per follows:

1. Run the following to validate the dataframe contents/structure and present the data in a way that makes it easy to copy the data for use in a GitHub Pull Request:

```py
oefdb.export_for_github(oefdb_df)
```

2. Go to https://github.com/climatiq/Open-Emission-Factors-DB/blob/main/OpenEmissionFactorsDB.csv
3. Click the "Edit this file" button.
4. Paste the copied data from above into the editor on GitHub.
5. Follow the instructions [here](https://github.com/climatiq/Open-Emission-Factors-DB/blob/main/CONTRIBUTING.md#2-create-a-pull-request) to create a Pull Request with your changes.

_Note_: If you are familiar with Git, you may instead benefit of cloning the [Open Emission Factors DB](https://github.com/climatiq/Open-Emission-Factors-DB) repo and exporting the changed dataframe as a file instead:

```py
oefdb.export_for_github(oefdb_df, export_path="/path/to/OpenEmissionFactorsDB.csv")
```

### Reviewing someone else's [OEFDB Pull Request](https://github.com/climatiq/Open-Emission-Factors-DB/pulls)

1. Use the number of the Pull Request in [OEFDB Pull Request](https://github.com/climatiq/Open-Emission-Factors-DB/pulls) when importing the data:

```py
oefdb_df_under_review = oefdb.import_from_github(pr=123)
```

2. Use Python to review the data, comparing it to the main revision data as necessary.
3. Add review comments via the GitHub UI as necessary and approve when discussions are resolved.

## Development

To work on improving this library, please read [DEV.md](./DEV.md).
