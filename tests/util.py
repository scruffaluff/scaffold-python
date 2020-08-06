"""Utility functions for testing."""


import pathlib
import re
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
