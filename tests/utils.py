from os.path import dirname, join, realpath

from pandas import DataFrame

fixtures_dir_path = join(dirname(realpath(__file__)), "fixtures")


def load_oefdb_fixture(ref: str) -> DataFrame:
    from oefdb import from_oefdb_csv

    return from_oefdb_csv(join(fixtures_dir_path, f"{ref}.csv"))
