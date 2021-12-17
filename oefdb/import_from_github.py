from io import BytesIO
from typing import Optional

from github import Repository
from pandas import DataFrame, read_csv

oefdb_csv_filename = "OpenEmissionFactorsDB.csv"


def import_from_github(
    pr: Optional[int] = None, repo_reference: str = "climatiq/Open-Emission-Factors-DB"
) -> DataFrame:
    if pr:
        return import_from_github_pr(pr, repo_reference=repo_reference)
    return import_from_github_main_branch(repo_reference=repo_reference)


def get_oefdb_repo(repo_reference: str) -> Repository:
    from github import Github

    g = Github()
    return g.get_repo(repo_reference)


def import_from_github_pr(number: int, repo_reference: str) -> DataFrame:
    repo = get_oefdb_repo(repo_reference)
    pr = repo.get_pull(number)
    return read_csv(get_oefdb_csv_contents(pr.head.repo, pr.head.ref))


def import_from_github_main_branch(repo_reference: str) -> DataFrame:
    repo = get_oefdb_repo(repo_reference)
    return read_csv(get_oefdb_csv_contents(repo))


def get_oefdb_csv_contents(repo: Repository, ref: Optional[str] = None) -> BytesIO:
    if ref:
        contents = repo.get_contents(oefdb_csv_filename, ref)
    else:
        contents = repo.get_contents(oefdb_csv_filename)
    return BytesIO(contents.decoded_content)
