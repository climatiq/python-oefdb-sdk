from io import BytesIO
from typing import Optional

import click
from github import (
    GitBlob,
    RateLimitExceededException,
    Repository,
    UnknownObjectException,
)
from pandas import DataFrame

oefdb_csv_filename = "OpenEmissionFactorsDB.csv"


def import_from_github(
    pr: Optional[int] = None, repo_reference: Optional[str] = None
) -> DataFrame:
    if repo_reference is None:
        repo_reference = "climatiq/Open-Emission-Factors-DB"
    try:
        if pr:
            return import_from_github_pr(pr, repo_reference=repo_reference)
        return import_from_github_main_branch(repo_reference=repo_reference)
    except RateLimitExceededException:
        raise Exception(
            "GitHub API rate limit exceeded. "
            "Check the python-oefdb-sdk README for instructions on how to avoid this."
        )


def get_oefdb_repo(repo_reference: str) -> Repository:
    import os

    from dotenv import load_dotenv
    from github import Github

    load_dotenv()

    github_login_or_token = os.environ.get("GH_TOKEN")
    g = Github(login_or_token=github_login_or_token)
    return g.get_repo(repo_reference)


def import_from_github_pr(number: int, repo_reference: str) -> DataFrame:
    from oefdb.util.from_oefdb_csv import from_oefdb_csv

    repo = get_oefdb_repo(repo_reference)
    pr = repo.get_pull(number)
    return from_oefdb_csv(get_oefdb_csv_bytes(pr.head.repo, pr.head.ref))


def import_from_github_main_branch(repo_reference: str) -> DataFrame:
    from oefdb.util.from_oefdb_csv import from_oefdb_csv

    repo = get_oefdb_repo(repo_reference)
    return from_oefdb_csv(get_oefdb_csv_bytes(repo))


def get_blob_content(repo: Repository, branch: str, path_name: str) -> GitBlob.GitBlob:
    ref = f"heads/{branch}"
    try:
        git_ref = repo.get_git_ref(ref)
        tree = repo.get_git_tree(git_ref.object.sha, recursive="/" in path_name).tree
        sha = [x.sha for x in tree if x.path == path_name]
        if not sha:
            raise Exception(
                f"The file '{path_name}' was not found in branch '{branch}'"
            )
        return repo.get_git_blob(sha[0])
    except UnknownObjectException:
        raise Exception(f"The branch '{branch}' was not found") from None


def get_oefdb_csv_bytes(repo: Repository, branch: Optional[str] = None) -> BytesIO:
    if branch is None:
        branch = "main"
    blob = get_blob_content(repo, branch, oefdb_csv_filename)

    if blob.encoding == "utf-8":
        blob_bytes = bytes(blob.content, "utf-8")
    else:
        from base64 import b64decode

        blob_bytes = b64decode(blob.content)

    return BytesIO(blob_bytes)


@click.command()
@click.option(
    "--output", "-o", required=True, type=str, help="OEFDB CSV file export path"
)
@click.option("--pr", "-p", default=None, type=int, help="OEFDB repo pull request id")
@click.option(
    "--repo_reference", "-r", default=None, type=str, help="OEFDB repo org and name"
)
def cli(
    output: str, pr: Optional[int] = None, repo_reference: Optional[str] = None
) -> None:
    import oefdb

    oefdb_df = oefdb.import_from_github(pr=pr, repo_reference=repo_reference)
    oefdb_csv = oefdb.to_oefdb_csv(oefdb_df)

    from oefdb.export_for_github import export_oefdb_csv_to_file

    export_oefdb_csv_to_file(oefdb_csv, output)
