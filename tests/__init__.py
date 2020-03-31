"""Tests for scaffold-python."""


import pathlib
from typing import List

import pytest
from pytest_cookies import plugin


def test_default(cookies: plugin.Cookies) -> None:
    """Check that default configuration generates correctly."""

    res = cookies.bake()

    assert res.exit_code == 0


def test_default_removed_paths(cookies: plugin.Cookies) -> None:
    """Check that default configuration generates correctly."""

    res = cookies.bake()

    project_path = pathlib.Path(res.project)
    path_names = [path.name for path in project_path.iterdir()]
    assert ".gitlab-ci.yaml" not in path_names


@pytest.mark.parametrize("features", [["basic"], ["cli"]])
def test_no_double_blank_lines(
    features: List[str], cookies: plugin.Cookies
) -> None:
    """Check that the created pyproject.toml file has no double blank lines."""

    context = {"features": features}
    res = cookies.bake(extra_context=context)

    pyproject_path = pathlib.Path(res.project) / "pyproject.toml"
    text = pyproject_path.read_text()
    assert "\n\n\n" not in text


@pytest.mark.parametrize("features", [["basic"], ["cli"]])
def test_no_trailing_blank_line(
    features: List[str], cookies: plugin.Cookies
) -> None:
    """Check that the pyproject.toml does not have a trailing blank line."""

    context = {"features": features}
    res = cookies.bake(extra_context=context)

    pyproject_path = pathlib.Path(res.project) / "pyproject.toml"
    text = pyproject_path.read_text()
    assert not text.endswith("\n\n")


def test_project_slug_invalid(cookies: plugin.Cookies) -> None:
    """Check that cookiecutter rejects invalid package names."""

    res = cookies.bake(extra_context={"project_name": "$Mock?"})

    assert res.exit_code == -1
