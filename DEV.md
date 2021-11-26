## Development

### Setting up the development environment

First, install Python 3.7+ and [Poetry](https://python-poetry.org/) on your system.

Then, install dependencies:

```
poetry install
```

This sets up a local Python environment with all the relevant dependencies.

The remaining commands in this readme assume you have activated it by running:

```
poetry shell
```

Now install the Git hooks that will make it harder to accidentally commit incorrectly formatted files:

```
pre-commit install
```

### Run tests, formatters and linters

Run tests, formatters and linters (using the currently active Python version):

```
poe test
```

#### Tests package

The package tests themselves are _outside_ of the main library code, in
the directory aptly named `tests`.

#### Running tests only

Run tests:

```
poe pytest
```

Run a specific test:

```
poe pytest tests/test_oefdb.py
```

Run tests against all supported Python environments:

```
tox -- test
```

### Development setup

#### Principles

* Simple for developers to get up-and-running
* Consistent style (`isort`, `black`, `flake8`)
* Future-proof (`pyupgrade`)
* Full type hinting (`mypy`)

#### Development tools

* `poetry` for dependency management
* `poethepoet` as local task runner
* `isort`, `black`, `pyupgrade` and `flake8` linting
* `pre-commit` to run linting
* `mypy` for type checking
* `tox` and GitHub Actions for tests and CI

#### CI

There is a `.github/workflows/test.yaml` file that is used
to run all the tests on GitHub against all supported Python versions.
