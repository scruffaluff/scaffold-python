"""Tests for scaffold-python."""


import pathlib
import re
from typing import Any, Dict, List

import pytest
from pytest_cookies import plugin

from tests.util import file_matches, run_command


def test_black_format(baked_project: plugin.Result) -> None:
    """Generated files must pass Black format checker."""

    res = run_command(f"black -l 80 --check {baked_project.project}")

    expected = 0
    actual = res.returncode
    assert actual == expected, res.stderr


def test_flake8_lints(baked_project: plugin.Result) -> None:
    """Generated files must pass Flake8 lints."""

    src_dir = baked_project.project / "src"
    test_dir = baked_project.project / "tests"
    res = run_command(f"flake8 {src_dir} {test_dir}")

    expected = 0
    actual = res.returncode
    assert actual == expected, res.stdout


@pytest.mark.parametrize(
    "context", [{"project_name": "$Mock?"}],
)
def test_invalid_context(
    context: Dict[str, Any], cookies: plugin.Cookies
) -> None:
    """Check that cookiecutter rejects invalid context arguments."""

    res = cookies.bake(extra_context=context)
    assert res.exit_code == -1


def test_mypy_type_checks(baked_project: plugin.Result) -> None:
    """Generated files must pass Mypy type checks."""

    src_dir = baked_project.project / "src"
    test_dir = baked_project.project / "tests"
    res = run_command(f"mypy {src_dir} {test_dir}")

    expected = 0
    actual = res.returncode
    assert actual == expected, res.stdout


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


def test_no_trailing_blank_line(baked_project: plugin.Result) -> None:
    """Check that generated files do not have a trailing blank line."""

    for path in file_matches(baked_project, r"^.*$"):
        text = path.read_text()
        assert not text.endswith("\n\n"), f"File {path} ends with a blank line."


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
