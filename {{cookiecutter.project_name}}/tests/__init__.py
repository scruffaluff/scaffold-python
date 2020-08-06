"""{{ cookiecutter.project_name }} testing package."""


import pathlib

import toml

import {{ cookiecutter.project_slug }}


def test_version() -> None:
    """Check that all the version tags are in sync."""

    toml_path = pathlib.Path("pyproject.toml")
    expected = toml.load(pyproject_path)["tool"]["poetry"]["version"]

    actual = {{ cookiecutter.project_slug }}.__version__
    assert actual == expected
