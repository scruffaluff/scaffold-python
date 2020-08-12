"""Utility functions for testing."""


import pathlib
import re
import subprocess
from typing import Iterator

from pytest_cookies.plugin import Result


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


def run_command(command: str) -> subprocess.CompletedProcess:
    """Execute shell command and capture output.

    Args:
        command: Shell command to execute.

    Raises:
        CalledProcessError: If shell command returns a non-zero exit code.

    Returns:
        Completed shell process information.
    """

    return subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
    )
