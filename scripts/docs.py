"""Script for building and serving documentation."""


import pathlib
import shutil
import subprocess

import typer


app = typer.Typer(help=__doc__)


@app.command()
def build() -> None:
    """Build the MkDocs documentation."""
    run("mkdocs build", "Failed to build project documentation.")


def run(command: str, error_msg: str) -> None:
    """Prepare documentation and run given command.

    Args:
        command: Command to execute after preparing documentation.
        error_msg: Error message if command fails.
    """
    repo_path = pathlib.Path(__file__).parents[1]

    copy_files(repo_path)

    try:
        subprocess.run(args=command, shell=True, check=True)
    except subprocess.CalledProcessError:
        typer.secho(f"Error: {error_msg}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


def copy_files(repo_path: pathlib.Path) -> None:
    """Sync documentation index with repository README file.

    Args:
        repo_path: Repository root path.
    """
    docs_dir = repo_path / "docs"
    if not docs_dir.exists():
        docs_dir.mkdir()

    paths = [("README.md", "docs/index.md")]

    for src, dest in paths:
        shutil.copy(src=repo_path / src, dst=repo_path / dest)


@app.command()
def gh_deploy() -> None:
    """Deploy your documentation to GitHub Pages."""
    run("mkdocs gh-deploy", "Failed to deploy project documentation.")


@app.command()
def serve() -> None:
    """Run the builtin development server."""
    run("mkdocs serve", "Failed to serve project documentation.")


if __name__ == "__main__":
    app()
