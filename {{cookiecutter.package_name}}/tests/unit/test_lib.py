"""Unit tests for library integration."""


import pathlib

import toml

import {{ cookiecutter.package_name }}


def test_version() -> None:
    """Check that all the version tags are in sync."""

    pyproject_path = pathlib.Path({{ cookiecutter.package_name }}.__file__).parents[2] / "pyproject.toml"
    expected = toml.load(pyproject_path)["tool"]["poetry"]["version"]

    actual = {{ cookiecutter.package_name }}.__version__
    assert actual == expected
