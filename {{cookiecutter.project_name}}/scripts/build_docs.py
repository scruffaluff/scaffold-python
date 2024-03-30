"""Copy index file and build documentation."""

from pathlib import Path
import shutil
import subprocess
from subprocess import CalledProcessError
import sys


def build_docs() -> None:
    """Build documentation with MkDocs."""
    try:
        subprocess.run(args="mkdocs build --strict", shell=True, check=True)
    except CalledProcessError:
        print("Failed to build project documentation.", sys.stderr)
        sys.exit(1)


def copy_files(repo_path: Path) -> None:
    """Sync documentation index with repository README file.

    Args:
        repo_path: Repository root path.
    """
    shutil.copy(src=repo_path / "README.md", dst=repo_path / "docs/index.md")

    for file_name in ["CONTRIBUTING.md", "LICENSE.md"]:
        shutil.copy(
            src=repo_path / file_name,
            dst=repo_path / f"docs/{file_name}",
        )


def main() -> None:
    """Entrypoint for documentation building."""
    repo_path = Path(__file__).parents[1]
    copy_files(repo_path)
    build_docs()


if __name__ == "__main__":
    main()
