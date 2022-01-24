from os.path import dirname, join, realpath

import pandas as pd
from pandas import DataFrame

fixtures_dir_path = join(dirname(realpath(__file__)), "fixtures")


def load_oefdb_fixture(ref: str) -> DataFrame:
    return pd.read_csv(join(fixtures_dir_path, f"{ref}.csv"))
