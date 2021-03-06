# ---
# jupyter:
#   jupytext:
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.3
#   kernelspec:
#     display_name: python-oefdb-sdk
#     language: python
#     name: python-oefdb-sdk
# ---

# makes edits in libs available without restarting the kernel
# %reload_ext autoreload
# %autoreload 2

import oefdb

oefdb_df = oefdb.import_from_github()
oefdb_df

oefdb.validate(oefdb_df)

oefdb.to_oefdb_csv(oefdb_df)

oefdb.export_for_github(oefdb_df)

# optional, run to increase the GitHub API rate limit
import getpass
import os

os.environ["GH_TOKEN"] = getpass.getpass()
