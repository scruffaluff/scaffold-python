"""{{ cookiecutter.project_name }} testing package."""


import pathlib

import toml

import {{ cookiecutter.project_slug }}
from tests import util


REPO_PATH = pathlib.Path(__file__).parents[1]


def test_matching_structure() -> None:
    """Test directories match structure of src directory."""
    src_path = REPO_PATH / "src/{{ cookiecutter.project_slug }}"
    test_path = REPO_PATH / "tests"

    error_msg = "Noe corresponding source code file {} for test file {}."

    for dir_name in ["integration", "unit"]:
        test_dir = test_path / dir_name
        for test_file in util.find_test_files(test_dir):
            src_file = src_path / util.remove_name_prefix(test_file, "test_")

            rel_src_file = src_file.relative_to(src_path)
            rel_test_file = (test_dir / test_file).relative_to(REPO_PATH)

            assert src_file.exists(), error_msg.format(
                rel_src_file, rel_test_file
            )


def test_version() -> None:
    """Check that all the version tags are in sync."""
    toml_path = REPO_PATH / "pyproject.toml"
    expected = toml.load(toml_path)["tool"]["poetry"]["version"]

    actual = {{ cookiecutter.project_slug }}.__version__
    assert actual == expected
