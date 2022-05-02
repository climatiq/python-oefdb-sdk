from __future__ import annotations

from io import BytesIO

import click
from github import (
    GitBlob,
    GitRef,
    RateLimitExceededException,
    Repository,
    UnknownObjectException,
)
from pandas import DataFrame

oefdb_csv_filename = "OpenEmissionFactorsDB.csv"


def import_from_github(
    pr: int | None = None, repo_reference: str | None = None
) -> DataFrame:
    try:
        (repo, git_ref) = get_commit_metadata(repo_reference, pr)
        commit_sha = git_ref.object.sha
        return import_oefdb_df_from_github(repo, commit_sha)
    except RateLimitExceededException:
        raise Exception(
            "GitHub API rate limit exceeded. "
            "Check the python-oefdb-sdk README for instructions on how to avoid this."
        )


def import_oefdb_df_from_github(
    repo: Repository.Repository, commit_sha: str
) -> DataFrame:
    from oefdb.util.from_oefdb_csv import from_oefdb_csv

    return from_oefdb_csv(get_oefdb_csv_bytes(repo, commit_sha))


def get_oefdb_repo(repo_reference: str) -> Repository.Repository:
    import os

    from dotenv import load_dotenv
    from github import Github

    load_dotenv()

    github_login_or_token = os.environ.get("GH_TOKEN")
    g = Github(login_or_token=github_login_or_token)
    return g.get_repo(repo_reference)


def get_commit_metadata(
    repo_reference: str | None,
    pr: int | None,
) -> tuple[Repository, GitRef.GitRef]:
    if repo_reference is None:
        repo_reference = "climatiq/Open-Emission-Factors-DB"
    repo = get_oefdb_repo(repo_reference)
    if pr:
        pull_request = repo.get_pull(pr)
        branch = pull_request.head.ref
    else:
        branch = "main"
    try:
        ref = f"heads/{branch}"
        git_ref = repo.get_git_ref(ref)
        return (repo, git_ref)
    except UnknownObjectException:
        raise Exception(
            f"The branch '{branch}' was not found in repo '{repo_reference}'"
        ) from None


def get_blob_content(
    repo: Repository.Repository, commit_sha: str, path_name: str
) -> GitBlob.GitBlob:
    try:
        tree = repo.get_git_tree(commit_sha, recursive="/" in path_name).tree
        matching_sha = [x.sha for x in tree if x.path == path_name]
        if not matching_sha:
            raise Exception(
                f"The file '{path_name}' was not found in commit '{commit_sha}'"
            )
        return repo.get_git_blob(matching_sha[0])
    except UnknownObjectException:
        raise Exception(f"The commit '{commit_sha}' was not found") from None


def get_oefdb_csv_bytes(repo: Repository.Repository, commit_sha: str) -> BytesIO:
    blob = get_blob_content(repo, commit_sha, oefdb_csv_filename)

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
def cli(output: str, pr: int | None = None, repo_reference: str | None = None) -> None:
    import oefdb

    oefdb_df = oefdb.import_from_github(pr=pr, repo_reference=repo_reference)
    oefdb_csv = oefdb.to_oefdb_csv(oefdb_df)

    from oefdb.export_for_github import export_oefdb_csv_to_file

    export_oefdb_csv_to_file(oefdb_csv, output)
