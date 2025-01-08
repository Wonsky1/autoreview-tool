from typing import List
from github.Repository import Repository


def get_all_repository_paths(repo: Repository, path: str = "") -> List[str]:
    paths = []
    contents = repo.get_contents(path)
    for content in contents:
        if content.type == "dir":
            paths.extend(get_all_repository_paths(repo, content.path))
        else:
            paths.append(content.path)
    return paths
