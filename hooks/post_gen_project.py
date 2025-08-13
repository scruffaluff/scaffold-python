"""Project post-generation hooks."""

from __future__ import annotations

import shutil
from pathlib import Path

Paths = list[Path]


PATHS: dict[str, Paths | dict[str, Paths]] = {
    "githost": {
        "github": [Path(".github")],
        "gitlab": [Path(".gitlab-ci.yml")],
    },
    "cli_support": [
        Path("src/{{ cookiecutter.project_slug }}/__main__.py"),
    ],
    "prettier_support": [
        Path(".prettierignore"),
        Path(".prettierrc.yaml"),
    ],
}


def clean_bool(chosen: str, paths: Paths) -> None:
    """Remove option paths if it was not chosen.

    Args:
        chosen: Whether option was chosen during scaffolding.
        paths: Paths to remove if option was not chosen.
    """
    if chosen != "yes":
        for path in paths:
            remove_path(path)


def clean_choice(choice: str, options: dict[str, Paths]) -> None:
    """Remove choice paths from unchosen options.

    Args:
        choice: Chosen option from list during scaffolding.
        options: Path contexts for list options.
    """
    for option, paths in options.items():
        if option != choice:
            for path in paths:
                remove_path(path)


def clean_paths(context: dict[str, str]) -> None:
    """Delete residual paths from project.

    Args:
        context: Chosen options from scaffolding prompt.
    """
    for key, val in PATHS.items():
        if isinstance(val, dict):
            clean_choice(context[key], val)
        elif isinstance(val, list):
            clean_bool(context[key], val)
        else:
            message = f"Unsupported type '{type(val)}' in PATHS data."
            raise TypeError(message)


def main() -> None:
    """Entrypoint for project post generation hooks."""
    context = {
        "githost": "{{ cookiecutter.githost }}",
        "cli_support": "{{ cookiecutter.cli_support }}",
        "prettier_support": "{{ cookiecutter.prettier_support }}",
        "pypi_support": "{{ cookiecutter.pypi_support }}",
    }
    clean_paths(context)


def remove_path(path: Path) -> None:
    """Delete file system path.

    Args:
        path: File system path to delete.
    """
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    elif path.exists():
        path.unlink()


if __name__ == "__main__":
    main()
