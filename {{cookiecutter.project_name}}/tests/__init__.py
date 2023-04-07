"""{{ cookiecutter.project_name }} testing package."""


import pathlib

import toml

import {{ cookiecutter.project_slug }}


REPO_PATH = pathlib.Path(__file__).parents[1]


def test_version() -> None:
    """Check that all the version tags are in sync."""
    toml_path = REPO_PATH / "pyproject.toml"
    expected = toml.load(toml_path)["tool"]["poetry"]["version"]

    actual = {{ cookiecutter.project_slug }}.__version__
    assert actual == expected
