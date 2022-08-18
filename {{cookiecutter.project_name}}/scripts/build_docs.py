"""Copy index file and build documentation."""


from pathlib import Path
import shutil
import subprocess
from subprocess import CalledProcessError
import sys


def build_docs() -> None:
    """Build documentation with MkDocs."""
    try:
        subprocess.run(args="mkdocs build", shell=True, check=True)
    except CalledProcessError:
        print("Failed to build project documentation.", sys.stderr)
        sys.exit(1)


def copy_index(repo_path: Path) -> None:
    """Sync documentation index with repository README file.

    Args:
        repo_path: Repository root path.
    """
    src_path = repo_path / "README.md"
    dest_path = repo_path / "docs/index.md"

    shutil.copy(src=src_path, dst=dest_path)


def main() -> None:
    """Entrypoint for documentation building."""
    repo_path = Path(__file__).parents[1]
    copy_index(repo_path)
    build_docs()


if __name__ == "__main__":
    main()
