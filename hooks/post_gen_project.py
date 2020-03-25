"""Project post generation hooks."""


import pathlib
import shutil
from typing import Dict, List


PATHS: Dict[str, Dict[str, List[pathlib.Path]]] = {
    "git_host": {
        "github": [pathlib.Path(".github")],
        "gitlab": [pathlib.Path(".gitlab-ci.yaml")],
    },
    "features": {
        "cli": [
            pathlib.Path("src/{{ cookiecutter.project_slug }}/__main__.py"),
        ],
        "prettier": [
            pathlib.Path(".prettierignore"),
            pathlib.Path("package.json"),
        ],
    },
}


def clean_paths(platform: str) -> None:
    """Delete residual paths from project.

    Args:
        platform: Git hosting platform.
    """

    for host, paths in PATHS["git_host"].items():
        if platform != host:
            for path in paths:
                remove_path(path)


def main() -> None:
    """Entrypoint for project post generation hooks."""

    git_host = "{{ cookiecutter.git_host }}"
    clean_paths(git_host)


def remove_path(path: pathlib.Path) -> None:
    """Delete file system path.

    Args:
        path: File system path to delete.
    """

    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        path.unlink()


if __name__ == "__main__":
    main()
