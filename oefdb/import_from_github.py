from io import BytesIO
from typing import Optional

from github import Repository
from pandas import DataFrame, read_csv

oefdb_csv_filename = "OpenEmissionFactorsDB.csv"


def import_from_github(pr: Optional[int] = None) -> DataFrame:
    if pr:
        return import_from_github_pr(pr)
    return import_from_github_main_branch()


def get_oefdb_repo(
    full_name_or_id: str = "climatiq/Open-Emission-Factors-DB",
) -> Repository:
    from github import Github

    g = Github()
    return g.get_repo(full_name_or_id)


def import_from_github_pr(number: int) -> DataFrame:
    repo = get_oefdb_repo()
    pr = repo.get_pull(number)
    return read_csv(get_oefdb_csv_contents(pr.head.repo, pr.head.ref))


def import_from_github_main_branch() -> DataFrame:
    repo = get_oefdb_repo()
    return read_csv(get_oefdb_csv_contents(repo))


def get_oefdb_csv_contents(repo: Repository, ref: Optional[str] = None) -> BytesIO:
    if ref:
        contents = repo.get_contents(oefdb_csv_filename, ref)
    else:
        contents = repo.get_contents(oefdb_csv_filename)
    return BytesIO(contents.decoded_content)
