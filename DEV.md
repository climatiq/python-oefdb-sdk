## Development

### Setting up the development environment

First, install Python 3.7+ and [Poetry](https://python-poetry.org/) on your system.

Then, install dependencies:

```
poetry install
```

This sets up a local Python environment with all the relevant dependencies, including the Development Tools listed further down in this readme.

The remaining commands in this readme assume you have activated the local Python environment by running:

```
poetry shell
```

(Note: This is equivalent of running `source <activate-venv-script>` if we were using `venv` instead of Poetry)

Now install the Git hooks that will make it harder to accidentally commit incorrectly formatted files:

```
pre-commit install
```

### Installing new dependencies added by collaborators

When new dependencies gets added/updated/removed (in `pyproject.toml`) by collaborators, you need to run the following to update the correct environment with the latest dependencies:

```
poetry update
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

### Using the development version of python-oefdb-sdk in a notebook

Run the following to install a Jupyter kernel and opening the example Jupyter notebook:

```
poe install_kernel
jupyter-notebook example-notebook.py
```

After selecting the `python-oefdb-sdk` kernel in Jupyter you should be able to interact with the development version as if it was installed via pip.

### Development setup

#### Principles

* Simple for developers to get up-and-running (`poetry`, `poethepoet`)
* Unit tests with test coverage reports (`pytest`, `tox`)
* Consistent style (`isort`, `black`, `flake8`)
* Prevent use of old Python syntax (`pyupgrade`)
* Require type hinting (`mypy`)

#### Development tools

* [`poetry`](https://python-poetry.org/) for dependency management
* [`poethepoet`](https://github.com/nat-n/poethepoet) as local task runner
* [`isort`](https://github.com/PyCQA/isort), [`black`](https://github.com/psf/black), [`pyupgrade`](https://github.com/asottile/pyupgrade) and [`flake8`](https://flake8.pycqa.org/en/latest/) linting
* [`mypy`](https://mypy.readthedocs.io/en/stable/) for type hinting
* [`pre-commit`](https://pre-commit.com/) to run linting / dependency checks
* [`pytest`](https://docs.pytest.org/), and [`tox`](https://tox.wiki) to run tests
* [`tox`]() and [GitHub Actions](https://github.com/features/actions) for running tests against different Python versions
* [`editorconfig`](https://editorconfig.org/) for telling the IDE how to format tabs/newlines etc

#### CI

There is a `.github/workflows/test.yaml` file that is used
to run all the tests on GitHub against all supported Python versions.

### Publishing

#### Preparations

To be able to publish new official versions of the package:

1. Register an account on [https://pypi.org]().
2. Get added as an Owner or Moderator.
3. Configure access locally:

```shell
poetry config pypi-token.pypi <your-pypi-token>
```

To test/verify publishing as a developer:

1. Register an account on [https://test.pypi.org]()
2. Add a token on [https://test.pypi.org/manage/account/token/]()
3. Configure access locally:

```shell
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi <your-pypi-token>
```

#### Release process

1. Create a new branch, called `release` and create a PR named `Release x.y.z`
2. Bump the semantic version number in [pyproject.toml](./pyproject.toml) and commit the change to the branch (Message: `Bump version to x.y.z`)
3. Build a new package with the updated version number:

```shell
poetry build
```

5. Dry-run publish via TestPyPi to verify that it works

```shell
poetry publish -r test-pypi
```

6. Check the README at TestPyPi etc to see that it is correct: https://test.pypi.org/project/oefdb/
7. Verify that the package installs and works properly in a new environment:

```shell
cd test-project
poetry env remove python
poetry update
```

8. Commit and changes and fixes
9. After verification, publish officially via PyPi:

```shell
poetry publish
```

10. Merge the PR after review approval.
