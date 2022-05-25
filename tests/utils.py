import csv
from os.path import dirname, join, realpath

from pandas import DataFrame

from oefdb.validators._typing import CsvRows

fixtures_dir_path = join(dirname(realpath(__file__)), "fixtures")


def load_oefdb_fixture_dataframe(ref: str) -> DataFrame:
    from oefdb import from_oefdb_csv

    return from_oefdb_csv(join(fixtures_dir_path, f"{ref}.csv"))


def load_oefdb_fixture_raw(ref: str) -> CsvRows:
    path = join(fixtures_dir_path, f"{ref}.csv")

    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        return list(reader)
