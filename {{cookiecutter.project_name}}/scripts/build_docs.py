"""Copy index file and build documentation."""


import pathlib
import shutil
import subprocess
import sys


def build_docs() -> None:
    """Build documentation with MkDocs."""

    try:
        subprocess.run(args="mkdocs build", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Failed to build project documentation.", sys.stderr)
        sys.exit(1)


def copy_index(repo_path: pathlib.Path) -> None:
    """Sync documentation index with repository README file.

    Args:
        repo_path: Repository root path.
    """

    src_path = repo_path / "docs/index.md"
    dest_path = repo_path / "README.md"

    shutil.copy(src=src_path, dst=dest_path)


def generate_cli_docs(repo_path: pathlib.Path) -> None:
    """Create documentation for the command line interface.

    Args:
        repo_path: Repository root path.
    """

    cli_doc = repo_path / "docs/src/cli/index.md"

    with cli_doc.open("w") as handle:
        try:
            subprocess.run(
                args="typer src/yamltable/__main__.py utils docs",
                shell=True,
                check=True,
                stdout=handle,
            )
        except subprocess.CalledProcessError:
            print(
                "Failed to build command line interface documentation.",
                sys.stderr,
            )
            sys.exit(1)


def main() -> None:
    """Entrypoint for documentation building."""

    repo_path = pathlib.Path(__file__).parents[1]
    copy_index(repo_path)
    generate_cli_docs(repo_path)
    build_docs()


if __name__ == "__main__":
    main()
