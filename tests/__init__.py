"""Tests for scaffold-python."""


import pathlib
import re
import subprocess
from typing import Any, Dict, List

import pytest
from pytest_cookies import plugin

from tests.util import file_matches


def test_black_format(baked_project: plugin.Result) -> None:
    """Generated files must pass Black format checker."""

    res = subprocess.run(
        f"black -l 80 --check {baked_project.project}",
        capture_output=True,
        shell=True,
    )

    expected = 0
    actual = res.returncode
    assert actual == expected, res.stderr


@pytest.mark.parametrize(
    "context", [{"project_name": "$Mock?"}],
)
def test_invalid_context(
    context: Dict[str, Any], cookies: plugin.Cookies
) -> None:
    """Check that cookiecutter rejects invalid context arguments."""

    res = cookies.bake(extra_context=context)
    assert res.exit_code == -1


def test_no_blank_lines(baked_project: plugin.Result) -> None:
    """Project files do not have whitespace only lines."""

    regex = re.compile(r"^\s+$")
    error_msg = "File {}, line {}: {} has whitespace."

    for path in file_matches(baked_project, r"^.*$"):
        for idx, line in enumerate(path.read_text().split("\n")):
            assert not regex.match(line), error_msg.format(path, idx, line)


def test_no_contiguous_blank_lines(baked_project: plugin.Result) -> None:
    """Project files do not have subsequent empty lines."""

    regex = re.compile(r"^\s+$")
    for path in file_matches(baked_project, r"^.*$"):
        text = path.read_text()
        assert not regex.match(text), f"File {path} has contiguous blank lines."


def test_no_starting_blank_line(baked_project: plugin.Result) -> None:
    """Check that generated files do not start with a blank line."""

    regex = re.compile(r"^\s*$")
    for path in file_matches(baked_project, r"^.*(?<!\.typed)$"):
        text = path.read_text().split("\n")[0]
        assert not regex.match(text), f"File {path} begins with a blank line."


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
