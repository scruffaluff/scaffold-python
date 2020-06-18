"""Tests for scaffold-python."""


import pathlib
import re
from typing import Any, Dict, List

import pytest
from pytest_cookies import plugin


@pytest.mark.parametrize(
    "context", [{"project_name": "$Mock?"}],
)
def test_invalid_context(
    context: Dict[str, Any], cookies: plugin.Cookies
) -> None:
    """Check that cookiecutter rejects invalid context arguments."""
    res = cookies.bake(extra_context=context)
    assert res.exit_code == -1


@pytest.mark.parametrize(
    "context,globs",
    [
        (
            {"githost": "github", "pypi_support": "yes"},
            [".github/workflows/*.yaml"],
        ),
        ({"githost": "gitlab", "prettier_support": "no"}, [".gitlab-ci.yml"]),
    ],
)
def test_no_blank_lines(
    context: Dict[str, Any], globs: List[str], cookies: plugin.Cookies
) -> None:
    """Check that specific files do not have blank lines."""
    res = cookies.bake(extra_context=context)
    repo_path = pathlib.Path(res.project)

    regex = re.compile(r"\n\s*\n")
    for glob in globs:
        for path in repo_path.glob(glob):
            text = path.read_text()
            assert not regex.search(text)


@pytest.mark.parametrize(
    "context,globs",
    [
        ({"license": "MIT"}, ["LICENSE.md"]),
        ({"license": "private"}, ["LICENSE.md"]),
        ({"cli_support": "yes"}, ["pyproject.toml"]),
        ({"cli_support": "no"}, ["pyproject.toml"]),
    ],
)
def test_no_double_blank_lines(
    context: Dict[str, Any], globs: List[str], cookies: plugin.Cookies
) -> None:
    """Check that generated files do not have double blank lines."""
    res = cookies.bake(extra_context=context)
    repo_path = pathlib.Path(res.project)

    regex = re.compile(r"\n\s*\n\s*\n")
    for glob in globs:
        for path in repo_path.glob(glob):
            text = path.read_text()
            assert not regex.search(text)


@pytest.mark.parametrize(
    "context,globs",
    [
        ({"license": "MIT"}, ["LICENSE.md"]),
        ({"license": "private"}, ["LICENSE.md"]),
        ({"cli_support": "yes"}, ["pyproject.toml"]),
    ],
)
def test_no_staring_blank_line(
    context: Dict[str, Any], globs: List[str], cookies: plugin.Cookies
) -> None:
    """Check that generated files do not have a trailing blank line."""
    res = cookies.bake(extra_context=context)
    repo_path = pathlib.Path(res.project)

    regex = re.compile(r"^\n\s*\n.*")
    for glob in globs:
        for path in repo_path.glob(glob):
            text = path.read_text()
            assert not regex.search(text)


@pytest.mark.parametrize(
    "context,globs",
    [
        ({"license": "MIT"}, ["LICENSE.md"]),
        ({"license": "private"}, ["LICENSE.md"]),
        ({"cli_support": "yes"}, ["pyproject.toml"]),
    ],
)
def test_no_trailing_blank_line(
    context: Dict[str, Any], globs: List[str], cookies: plugin.Cookies
) -> None:
    """Check that generated files do not have a trailing blank line."""
    res = cookies.bake(extra_context=context)
    repo_path = pathlib.Path(res.project)

    for glob in globs:
        for path in repo_path.glob(glob):
            assert not path.read_text().endswith("\n\n")


@pytest.mark.parametrize(
    "context,paths",
    [
        ({"githost": "github"}, [".gitlab-ci.yml"]),
        ({"githost": "gitlab"}, [".github"]),
        (
            {"project_slug": "mock", "cli_support": "no"},
            ["src/mock/__main__.py"],
        ),
        ({"docker_support": "no"}, [".dockerignore", "Dockerfile"]),
        ({"prettier_support": "no"}, [".prettierignore", "package.json"]),
        ({"pypi_support": "no"}, [".github/workflow/publish.yaml"]),
    ],
)
def test_removed_paths(
    context: Dict[str, Any], paths: List[str], cookies: plugin.Cookies
) -> None:
    """Check that specific paths are removed after scaffolding."""
    res = cookies.bake(extra_context=context)

    project_path = pathlib.Path(res.project)
    scaffold_paths = [path for path in project_path.rglob("*")]

    for path in paths:
        remove_path = project_path / path
        assert remove_path not in scaffold_paths


@pytest.mark.parametrize(
    "context,path,text",
    [
        ({"license": "private"}, "LICENSE.md", "free of charge"),
        ({"cli_support": "no"}, "pyproject.toml", "typer-cli"),
        ({"prettier_support": "no"}, ".github/workflows/build.yaml", "npm"),
    ],
)
def test_removed_text(
    context: Dict[str, Any], path: str, text: str, cookies: plugin.Cookies
) -> None:
    """Check that generated files do not have double blank lines."""
    res = cookies.bake(extra_context=context)
    repo_path = pathlib.Path(res.project)

    contents = (repo_path / path).read_text()
    assert text not in contents


@pytest.mark.parametrize(
    "context",
    [
        {"githost": "github"},
        {"githost": "gitlab"},
        {"os": "linux"},
        {"os": "macos"},
        {"os": "windows"},
        {"cli_support": "yes"},
        {"cli_support": "no"},
        {"docker_support": "yes"},
        {"docker_support": "no"},
        {"prettier_support": "yes"},
        {"prettier_support": "no"},
        {"pypi_support": "yes"},
        {"pypi_support": "no"},
    ],
)
def test_scaffold(context: Dict[str, Any], cookies: plugin.Cookies) -> None:
    """Check that various configurations generate successfully."""
    res = cookies.bake(extra_context=context)
    assert res.exit_code == 0
