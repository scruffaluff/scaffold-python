"""Sort repository's pyproject.toml file."""


from collections import OrderedDict
from pathlib import Path
from typing import Any, MutableMapping

import toml


def sort_nested_dict(mmap: MutableMapping[str, Any]) -> OrderedDict:
    """Sorted nested dictionary by key.

    Args:
        dict_: Mapping to mutate by sorting.

    Returns:
        Sorted map.
    """

    for key, val in mmap.items():
        if isinstance(val, dict):
            mmap[key] = sort_nested_dict(val)

    return OrderedDict(sorted(mmap.items()))


def main() -> None:
    """Entrypoint for pyproject.toml file sorting."""

    repo_path = Path(__file__).parents[1]
    file_path = repo_path / "pyproject.toml"

    with file_path.open("r") as handle:
        unsorted_dict = toml.load(handle)

    sorted_dict = sort_nested_dict(unsorted_dict)
    with file_path.open("w") as handle:
        toml.dump(sorted_dict, handle)


if __name__ == "__main__":
    main()
