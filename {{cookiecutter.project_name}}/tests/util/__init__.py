"""Tools and utilites for testing."""


import pathlib
import re
from typing import Iterator


def find_test_files(test_dir: pathlib.Path) -> Iterator[pathlib.Path]:
    """Find all test files that will be executed by Pytest.

    Args:
        test_dir: Parent directory of test files.

    Returns:
        Test paths relative to test_dir.
    """

    regex = re.compile(r"^(__init__|test_.*).py$")
    for file_path in test_dir.rglob("*"):
        if regex.match(file_path.name):
            yield file_path.relative_to(test_dir)


def remove_name_prefix(path: pathlib.Path, prefix: str) -> pathlib.Path:
    """Remove prefix from path name.

    Does nothing if prefix is not part of path name.

    Args:
        path: File system path to edit.
        prefix: String prefix to remove from path name.

    Returns:
        Path without name prefix.
    """

    name = path.name[path.name.startswith(prefix) and len(prefix) :]
    return path.parent / name
