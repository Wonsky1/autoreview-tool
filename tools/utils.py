from typing import List, Optional
from github.Repository import Repository


def get_all_repository_paths(repo: Repository, path: str = "") -> List[str]:
    """
    Get all file paths in a GitHub repository.

    :param repo: The GitHub repository object.
    :param path: The path within the repository to start from (default is root).
    :return: A list of all file paths in the repository.
    """
    paths = []
    contents = repo.get_contents(path)

    for content in contents:
        if content.type == "dir":
            paths.extend(get_all_repository_paths(repo, content.path))
        else:
            paths.append(content.path)
    return paths
