"""Unit tests for library integration."""


import pathlib

import toml

import {{ cookiecutter.project_slug }}


def test_version() -> None:
    """Check that all the version tags are in sync."""

    # Check for pyproject.toml in two places in case of nonlocal install.
    toml_path = pathlib.Path("pyproject.toml")
    if toml_path.exists():
        pyproject_path = toml_path
    else:
        pyproject_path = pathlib.Path({{ cookiecutter.project_slug }}.__file__).parents[2] / "pyproject.toml"
    expected = toml.load(pyproject_path)["tool"]["poetry"]["version"]

    actual = {{ cookiecutter.project_slug }}.__version__
    assert actual == expected
