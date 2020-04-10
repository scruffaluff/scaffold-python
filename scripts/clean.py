"""Script for cleaing unversioned files."""


import pathlib
import re
import shutil
from typing import Iterable, List

import typer


app = typer.Typer(help=__doc__)


@app.command()
def clean(
    dry_run: bool = typer.Option(
        False, help="Show paths that would be removed but do not clean."
    )
) -> None:
    """Remove unversioned files from project."""
    rules = ignore_rules()
    paths = ignore_paths(rules)

    if dry_run:
        for path in paths:
            typer.secho(str(path), fg=typer.colors.GREEN)
    else:
        remove_paths(paths)


def ignore_paths(rules: Iterable[str]) -> List[pathlib.Path]:
    """Convert ignore rules into file paths.

    Args:
        rules: Iterable of Git ignore rules.

    Returns:
        Git ignored paths.
    """
    paths = (pathlib.Path(rule.replace("*", "")) for rule in rules)
    return [path for path in paths if path.exists()]


def ignore_rules() -> List[str]:
    """Find all root level ignore rules.

    A root level ignore rule is one that does not begin with *, i.e. specifies
    a path which begins at the root of the repository.

    Returns:
        List of all root level ignore rules.
    """
    repo_path = pathlib.Path(__file__).parents[1]
    file_path = repo_path / ".gitignore"

    rules = file_path.read_text().splitlines()

    regex = re.compile(r"^[^*\s].*$")
    return list(filter(regex.match, rules))


def remove_paths(paths: Iterable[pathlib.Path]) -> None:
    """Remove given directory and file paths.

    Args:
        paths: System paths to remove.

    Raises:
        ValueError: If path is not a file or directory.
    """
    for path in paths:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)


if __name__ == "__main__":
    app()
