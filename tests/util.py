"""Utility functions for testing."""


import contextlib
import os
import pathlib
import re
import subprocess
from typing import Iterator, Optional

from pytest_cookies.plugin import Result


@contextlib.contextmanager
def chdir(dest_dir: pathlib.Path) -> Iterator[None]:
    """Context manager for changing the current working directory.

    Args:
        dest_dir: Directory to temporarily make the current directory.
    """

    src_dir = pathlib.Path.cwd()

    try:
        os.chdir(dest_dir)
        yield
    finally:
        os.chdir(src_dir)


def file_matches(bake: Result, regex_str: str) -> Iterator[pathlib.Path]:
    """Find all files in a directory whose name matches a regex.

    Args:
        dir_path: Directory to search for files.
        regex_str: Regex string for file names to satisfy.

    Yields:
        Matching file paths.
    """

    project_path = pathlib.Path(bake.project)
    regex = re.compile(regex_str)

    for path in project_path.rglob("*"):
        if path.is_file() and regex.match(path.name):
            yield path


def run_command(
    command: str, work_dir: Optional[pathlib.Path] = None
) -> subprocess.CompletedProcess:
    """Execute shell command in another directory and capture output.

    Args:
        command: Shell command to execute.
        work_dir: Location to make temporary working directory for command.

    Raises:
        CalledProcessError: If shell command returns a non-zero exit code.

    Returns:
        Completed shell process information.
    """

    work_dir = pathlib.Path.cwd() if work_dir is None else work_dir
    with chdir(work_dir):
        return subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
        )
