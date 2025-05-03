"""Project generation tests."""

import re
import sys
from typing import Any, Dict, List

import pytest
from pytest import mark
from pytest_cookies.plugin import Cookies, Result

from test import util


@mark.parametrize(
    "context",
    [
        {"githost": "github"},
        {"githost": "gitlab"},
        {"pypi_support": "yes"},
        {"pypi_support": "no"},
    ],
)
def test_badges_separate_lines(context: Dict[str, Any], cookies: Cookies) -> None:
    """Readme files must have all badge links on separate lines."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0, str(result.exception)
    readme = result.project_path / "README.md"

    regex = re.compile(r"img\.shields\.io")
    for line in readme.read_text().split("\n"):
        assert len(regex.findall(line)) < 2


@mark.parametrize(
    "context,paths",
    [
        ({"githost": "github"}, [".github"]),
        ({"githost": "gitlab"}, [".gitlab-ci.yml"]),
        (
            {"project_slug": "mock", "cli_support": "yes"},
            ["src/mock/__main__.py"],
        ),
        ({"prettier_support": "yes"}, [".prettierignore", ".prettierrc.yaml"]),
        ({"pypi_support": "yes"}, [".github/workflows/main.yaml"]),
    ],
)
def test_existing_paths(
    context: Dict[str, Any], paths: List[str], cookies: Cookies
) -> None:
    """Check that specific paths exist after scaffolding."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0, str(result.exception)
    for path in paths:
        file_path = result.project_path / path
        assert file_path.exists()


@mark.parametrize(
    "context,expected",
    [
        (
            {
                "githost": "gitlab",
                "project_repository": "https://gitlab.com/user/repository",
            },
            "https://user.gitlab.io/repository",
        ),
        (
            {
                "githost": "gitlab",
                "project_repository": "https://gitlab.com/group/subgroup/repository",
            },
            "https://group.gitlab.io/subgroup/repository",
        ),
    ],
)
def test_homepage_context(
    context: Dict[str, Any], expected: str, cookies: Cookies
) -> None:
    """Default homepage is generated from repository URL."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0, str(result.exception)
    actual = result.context["project_homepage"]
    assert actual == expected


@mark.parametrize(
    "context",
    [{"project_name": "$Mock?"}],
)
def test_invalid_context(context: Dict[str, Any], cookies: Cookies) -> None:
    """Check that cookiecutter rejects invalid context arguments."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == -1


def test_mkdocs_build(cookies: Cookies) -> None:
    """Mkdocs must be able to build documentation for baked project."""
    result = cookies.bake(extra_context={})
    assert result.exit_code == 0, str(result.exception)
    util.run_command(["uv", "sync"], cwd=result.project_path)
    util.run_command(["just", "doc"], cwd=result.project_path)


def test_mypy_type_checks(baked_project: Result) -> None:
    """Generated files must pass Mypy type checks."""
    util.run_command(
        ["uv", "run", "mypy", "."], cwd=baked_project.project_path, stream="stdout"
    )


def test_no_blank_lines(baked_project: Result) -> None:
    """Project files do not have whitespace only lines."""
    regex = re.compile(r"^\s+$")
    error_msg = "File {}, line {}: {} has whitespace."

    for path in util.file_matches(baked_project, r"^.*$"):
        for idx, line in enumerate(path.read_text().split("\n")):
            match = regex.match(line)
            assert match is None, error_msg.format(path, idx, line)


def test_no_contiguous_blank_lines(baked_project: Result) -> None:
    """Project files do not have subsequent empty lines."""
    regex = re.compile(r"\n\s*\n\s*\n")
    for path in util.file_matches(baked_project, r"^.*(?<!.py)$"):
        text = path.read_text()

        match = regex.search(text)
        assert match is None, f"File {path} has contiguous blank lines."


def test_no_starting_blank_line(baked_project: Result) -> None:
    """Check that generated files do not start with a blank line."""
    regex = re.compile(r"^\s*$")
    for path in util.file_matches(baked_project, r"^.*(?<!\.typed)$"):
        text = path.read_text().split("\n")[0]
        assert not regex.match(text), f"File {path} begins with a blank line."


def test_no_trailing_blank_line(baked_project: Result) -> None:
    """Check that generated files do not have a trailing blank line."""
    regex = re.compile(r"\n\s*$")
    for path in util.file_matches(baked_project, r"^.*$"):
        text = path.read_text()

        match = regex.match(text)
        assert match is None, f"File {path} ends with a blank line."


@mark.skipif(
    sys.platform in ["darwin", "win32"],
    reason="""
    Cookiecutter does not generate files with Windows line endings and Prettier
    returns nonzero exit codes on success for MacOS.
    """,
)
def test_prettier_format(baked_project: Result) -> None:
    """Generated files must pass Prettier format checker."""
    if baked_project.context["prettier_support"] == "no":
        pytest.skip("Prettier support is required for format testing.")
    util.run_command(
        [
            "deno",
            "run",
            "--allow-all",
            "npm:prettier",
            "--check",
            ".",
        ],
        cwd=baked_project.project_path,
    )


def test_pytest_test(cookies: Cookies) -> None:
    """Generated files must pass Pytest unit tests."""
    result = cookies.bake(extra_context={})
    assert result.exit_code == 0, str(result.exception)
    util.run_command(["uv", "sync"], cwd=result.project_path)
    util.run_command(["uv", "run", "pytest"], cwd=result.project_path, stream="stdout")


@mark.parametrize(
    "context,paths",
    [
        ({"githost": "github"}, [".gitlab-ci.yml"]),
        ({"githost": "gitlab"}, [".github"]),
        (
            {"project_slug": "mock", "cli_support": "no"},
            ["src/mock/__main__.py"],
        ),
        ({"prettier_support": "no"}, [".prettierignore", ".prettierrc.yaml"]),
    ],
)
def test_removed_paths(
    context: Dict[str, Any], paths: List[str], cookies: Cookies
) -> None:
    """Check that specific paths are removed after scaffolding."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0, str(result.exception)
    for path in paths:
        remove_path = result.project_path / path
        assert not remove_path.exists()


def test_ruff_format(baked_project: Result) -> None:
    """Generated files must pass Ruff format checker."""
    util.run_command(
        ["uv", "run", "ruff", "format", "--check", "."], cwd=baked_project.project_path
    )


def test_ruff_lint(baked_project: Result) -> None:
    """Generated files must pass Ruff lints."""
    util.run_command(
        ["uv", "run", "ruff", "check", "."], cwd=baked_project.project_path
    )


@mark.parametrize(
    "context",
    [
        {"githost": "github"},
        {"githost": "gitlab"},
        {"cli_support": "yes"},
        {"cli_support": "no"},
        {"prettier_support": "yes"},
        {"prettier_support": "no"},
        {"pypi_support": "yes"},
        {"pypi_support": "no"},
    ],
)
def test_scaffold(context: Dict[str, Any], cookies: Cookies) -> None:
    """Check that various configurations generate successfully."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0, str(result.exception)


@mark.parametrize(
    "context,paths,text,exist",
    [
        (
            {"prettier_support": "yes"},
            ["justfile"],
            "prettier",
            True,
        ),
        (
            {"prettier_support": "no"},
            ["justfile"],
            "prettier",
            False,
        ),
        (
            {"githost": "github", "pypi_support": "no"},
            ["README.md"],
            "pypi",
            False,
        ),
    ],
)
def test_text_existence(
    context: Dict[str, Any],
    paths: List[str],
    text: str,
    exist: bool,
    cookies: Cookies,
) -> None:
    """Check for existence of text in files."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0, str(result.exception)
    for path in paths:
        text_exists = text in (result.project_path / path).read_text()
        assert text_exists == exist


def test_toml_blank_lines(baked_project: Result) -> None:
    """Check that TOML files do not have blank lines not followed by a [."""
    regex = re.compile(r"\n\s*\n[^[]")
    for path in util.file_matches(baked_project, r"^.*\.toml$"):
        text = path.read_text()
        match = regex.search(text)
        assert match is None, f"TOML file {path} contains blank lines."
