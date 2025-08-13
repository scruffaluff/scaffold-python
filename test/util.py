"""Utility functions for testing."""

from __future__ import annotations

import contextlib
import os
import re
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from re import Match

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
    command: Sequence[str], cwd: Path | None = None, stream: str = "stderr"
) -> CompletedProcess:
    """Test command with helpful error messages.

    Args:
        command: Command to execute.
        cwd: Location to make temporary working directory for command.
        stream: Error message output stream.

    Returns:
        Completed shell process information.
    """
    process = subprocess.run(  # noqa: PLW1510
        command,
        capture_output=True,
        cwd=cwd,
    )
    assert process.returncode == 0, getattr(process, stream).decode("utf-8")
    return process


def show(match: Match) -> None:
    """Show lines surrounding regex match.

    Args:
        match: Regex match.
        text: Text parsed by regular expression.
    """
    text = match.string
    start, stop = match.span()

    m = re.match(r"\n.*$", text[:start])
    before = "" if m is None else m.string[m.start() : m.end()]
    m = re.match(r"^.*\n", text[stop:])
    after = "" if m is None else m.string[m.start() : m.end()]

    lines = before + text[start:stop] + after
    print(lines)
