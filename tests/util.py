"""Utility functions for testing."""

import contextlib
import os
from pathlib import Path
import re
import subprocess
from typing import Any, Iterator, Optional

from pytest_cookies.plugin import Result


@contextlib.contextmanager
def chdir(dest_dir: Path) -> Iterator[None]:
    """Context manager for changing the current working directory.

    Args:
        dest_dir: Directory to temporarily make the current directory.
    """
    # Needs to be called before try statement since current directory can change
    # inside a context manager.
    source_directory = Path.cwd()

    try:
        os.chdir(dest_dir)
        yield
    finally:
        os.chdir(source_directory)


def file_matches(baked_project: Result, regex_str: str) -> Iterator[Path]:
    """Find all files in a directory whose name matches a regex.

    Args:
        baked_project: Directory to search for files.
        regex_str: Regex string for file names to satisfy.

    Yields:
        Matching file paths.
    """
    regex = re.compile(regex_str)
    for path in baked_project.project_path.rglob("*"):
        if path.is_file() and regex.match(path.name):
            yield path


def run_command(
    command: str, work_dir: Optional[Path] = None
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
    directory = Path.cwd() if work_dir is None else work_dir
    with chdir(directory):
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )


def show(match: Any) -> None:
    """Show lines surrounding regex match.

    Args:
        match: Regex match.
        text: Text parsed by regular expression.
    """
    text = match.string
    start, stop = match.span()

    m = re.match(r"\n.*$", text[:start])
    if m is None:
        before = ""
    else:
        before = m.string[m.start() : m.end()]

    m = re.match(r"^.*\n", text[stop:])
    if m is None:
        after = ""
    else:
        after = m.string[m.start() : m.end()]

    lines = before + text[start:stop] + after
    print(lines)
