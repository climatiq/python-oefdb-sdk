from typing import Optional

from github import Repository


def import_from_github(pr: Optional[int] = None) -> bytes:
    if pr:
        return import_from_github_pr(pr)
    return import_from_github_main_branch()


def get_oefdb_repo(
    full_name_or_id: str = "climatiq/Open-Emission-Factors-DB",
) -> Repository:
    from github import Github

    g = Github()
    return g.get_repo(full_name_or_id)


def import_from_github_pr(number: int) -> bytes:
    repo = get_oefdb_repo()
    pr = repo.get_pull(number)
    return get_oefdb_csv_contents(pr.head.repo)


def import_from_github_main_branch() -> bytes:
    repo = get_oefdb_repo()
    return get_oefdb_csv_contents(repo)


def get_oefdb_csv_contents(repo: Repository) -> bytes:
    contents = repo.get_contents("OpenEmissionFactorsDB.csv")
    return contents.decoded_content
