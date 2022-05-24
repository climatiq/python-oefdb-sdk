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

## Command line scripts

### Import from GitHub

```shell
oefdb_import_from_github --output <oefdb-csv-file-save-path> [--pr <pull-request-id>]
```

### Validate an OEFDB CSV file

```shell
oefdb_validate --input <path-to-oefdb-csv-file>
```

### Export an OEFDB CSV file

```shell
oefdb_export_for_github --input <path-to-oefdb-csv-file> --output <oefdb-csv-file-export-path>
```

## FAQ

### Why am I getting an `github.GithubException.RateLimitExceededException` error?

This library uses the GitHub API to import OEFDB data and the API has a rate limit and you may run into `github.GithubException.RateLimitExceededException: 403 {"message": "API rate limit exceeded for 62.78.170.105. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)", "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"}`. By waiting or by authenticating with the API, this limit can be avoided/raised.

#### Authenticating with the GitHub API

1. Go to [https://github.com/settings/tokens/new]() to create a read-only personal access token. No checkboxes needs to be checked.

2. Call it something like `oefdb-github-api-token` and press `Generate token`.

3. Make sure to click the Copy-icon to copy the token (it is too easy to accidentally select some strange whitespace when selecting the token text)

4. Add your token to the `GH_TOKEN` env var.

In a notebook, you can do this via:

```py
import os
os.environ['GH_TOKEN'] = "foo123"
```

Or, in a shared notebook:
```py
import os
import getpass
os.environ['GH_TOKEN'] = getpass.getpass()
```

Alternatively, you can add a file called `.env` to the notebook's working directory and fill it with `GH_TOKEN=your-token`.

## Development

To work on improving this library, please read [DEV.md](./DEV.md).
