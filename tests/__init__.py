"""Tests for Scaffold Python."""


import pathlib
import re
import sys
from typing import Any, Dict, List

import pytest
from pytest_cookies import plugin

# Ingoring unused import for show_match. Function is imported for convenient
# test debugging.
from tests.util import file_matches, run_command, show  # noqa: F401


@pytest.mark.parametrize(
    "context",
    [
        {"githost": "github"},
        {"githost": "gitlab"},
        {"pypi_support": "yes"},
        {"pypi_support": "no"},
    ],
)
def test_badges_separate_lines(
    context: Dict[str, Any], cookies: plugin.Cookies
) -> None:
    """Readme files must have all badge links on separate lines."""

    res = cookies.bake(extra_context=context)
    readme = res.project_path / "README.md"

    regex = re.compile(r"img\.shields\.io")
    for line in readme.read_text().split("\n"):
        assert len(regex.findall(line)) < 2


def test_black_format(baked_project: plugin.Result) -> None:
    """Generated files must pass Black format checker."""

    proj_dir = baked_project.project_path
    proc = run_command(command="black -l 80 --check .", work_dir=proj_dir)

    expected = 0
    actual = proc.returncode
    assert actual == expected, proc.stderr.decode("utf-8")


@pytest.mark.parametrize(
    "context,paths",
    [
        ({"githost": "github"}, [".github"]),
        ({"githost": "gitlab"}, [".gitlab-ci.yml"]),
        (
            {"project_slug": "mock", "cli_support": "yes"},
            ["src/mock/__main__.py"],
        ),
        ({"prettier_support": "yes"}, [".prettierignore", ".prettierrc.yaml"]),
        ({"pypi_support": "yes"}, [".github/workflows/release.yaml"]),
    ],
)
def test_existing_paths(
    context: Dict[str, Any], paths: List[str], cookies: plugin.Cookies
) -> None:
    """Check that specific paths exist after scaffolding."""

    res = cookies.bake(extra_context=context)

    project_path = res.project_path
    for path in paths:
        file_path = project_path / path
        assert file_path.exists()


def test_flake8_lints(baked_project: plugin.Result) -> None:
    """Generated files must pass Flake8 lints."""

    proj_dir = baked_project.project_path
    src_dir = proj_dir / "src"
    test_dir = proj_dir / "tests"

    proc = run_command(
        command=f"flake8 {src_dir} {test_dir}", work_dir=proj_dir
    )

    expected = 0
    actual = proc.returncode
    # Flake8 prints errors to stdout instead of stderr.
    assert actual == expected, proc.stdout.decode("utf-8")


@pytest.mark.parametrize(
    "context",
    [{"project_name": "$Mock?"}],
)
def test_invalid_context(
    context: Dict[str, Any], cookies: plugin.Cookies
) -> None:
    """Check that cookiecutter rejects invalid context arguments."""

    res = cookies.bake(extra_context=context)
    assert res.exit_code == -1


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Poetry install command hits permission errors for temporary paths.",
)
def test_mkdocs_build(cookies: plugin.Cookies) -> None:
    """Mkdocs must be able to build documentation for baked project."""

    res = cookies.bake(extra_context={})
    proj_dir = res.project_path
    expected = 0

    proc = run_command(command="poetry install", work_dir=proj_dir)
    # Poetry prints errors to stdout instead of stderr.
    assert proc.returncode == expected, proc.stdout.decode("utf-8")

    proc = run_command(command="poetry run mkdocs build", work_dir=proj_dir)
    assert proc.returncode == expected, proc.stderr.decode("utf-8")


def test_mypy_type_checks(baked_project: plugin.Result) -> None:
    """Generated files must pass Mypy type checks."""

    proj_dir = baked_project.project_path
    src_dir = proj_dir / "src"
    test_dir = proj_dir / "tests"

    proc = run_command(
        command=f"mypy --install-types --non-interactive {src_dir} {test_dir}",
        work_dir=proj_dir,
    )

    expected = 0
    actual = proc.returncode
    # Mypy prints errors to stdout instead of stderr.
    assert actual == expected, proc.stdout.decode("utf-8")


def test_no_blank_lines(baked_project: plugin.Result) -> None:
    """Project files do not have whitespace only lines."""

    regex = re.compile(r"^\s+$")
    error_msg = "File {}, line {}: {} has whitespace."

    for path in file_matches(baked_project, r"^.*$"):
        for idx, line in enumerate(path.read_text().split("\n")):
            match = regex.match(line)
            assert match is None, error_msg.format(path, idx, line)


def test_no_contiguous_blank_lines(baked_project: plugin.Result) -> None:
    """Project files do not have subsequent empty lines."""

    regex = re.compile(r"\n\s*\n\s*\n")
    for path in file_matches(baked_project, r"^.*(?<!.py)$"):
        text = path.read_text()

        match = regex.search(text)
        assert match is None, f"File {path} has contiguous blank lines."


def test_no_starting_blank_line(baked_project: plugin.Result) -> None:
    """Check that generated files do not start with a blank line."""

    regex = re.compile(r"^\s*$")
    for path in file_matches(baked_project, r"^.*(?<!\.typed)$"):
        text = path.read_text().split("\n")[0]
        assert not regex.match(text), f"File {path} begins with a blank line."


def test_no_trailing_blank_line(baked_project: plugin.Result) -> None:
    """Check that generated files do not have a trailing blank line."""

    regex = re.compile(r"\n\s*$")
    for path in file_matches(baked_project, r"^.*$"):
        text = path.read_text()

        match = regex.match(text)
        assert match is None, f"File {path} ends with a blank line."


@pytest.mark.skipif(
    sys.platform in ["darwin", "win32"],
    reason="""
    Cookiecutter does not generate files with Windows line endings and Prettier
    returns nonzero exit codes on success for MacOS.
    """,
)
def test_prettier_format(cookies: plugin.Cookies) -> None:
    """Generated files must pass Prettier format checker."""

    res = cookies.bake(extra_context={})
    proj_dir = res.project_path

    proc = run_command(command="prettier --check .", work_dir=proj_dir)
    assert proc.returncode == 0, proc.stderr.decode("utf-8")


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Poetry install command hits permission errors for temporary paths.",
)
def test_pytest_test(cookies: plugin.Cookies) -> None:
    """Generated files must pass Pytest unit tests."""

    res = cookies.bake(extra_context={})
    proj_dir = res.project_path
    expected = 0

    proc = run_command(command="poetry install", work_dir=proj_dir)
    # Poetry prints errors to stdout instead of stderr.
    assert proc.returncode == expected, proc.stdout.decode("utf-8")

    proc = run_command(command="poetry run pytest", work_dir=proj_dir)
    # Pytest prints errors to stdout instead of stderr.
    assert proc.returncode == expected, proc.stdout.decode("utf-8")


@pytest.mark.parametrize(
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
    context: Dict[str, Any], paths: List[str], cookies: plugin.Cookies
) -> None:
    """Check that specific paths are removed after scaffolding."""

    res = cookies.bake(extra_context=context)

    project_path = res.project_path
    for path in paths:
        remove_path = project_path / path
        assert not remove_path.exists()


@pytest.mark.parametrize(
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
def test_scaffold(context: Dict[str, Any], cookies: plugin.Cookies) -> None:
    """Check that various configurations generate successfully."""

    res = cookies.bake(extra_context=context)
    assert res.exit_code == 0


@pytest.mark.parametrize(
    "context,paths,text,exist",
    [
        (
            {"githost": "gitlab", "prettier_support": "yes"},
            [".gitlab-ci.yml"],
            "prettier",
            True,
        ),
        (
            {"githost": "github", "prettier_support": "yes"},
            [".github/workflows/build.yaml"],
            "prettier",
            True,
        ),
        (
            {"githost": "gitlab", "prettier_support": "no"},
            [".gitlab-ci.yml"],
            "prettier",
            False,
        ),
        (
            {"githost": "github", "prettier_support": "no"},
            [".github/workflows/build.yaml"],
            "prettier",
            False,
        ),
        (
            {"githost": "github", "pypi_support": "yes"},
            [".github/workflows/release.yaml"],
            "pypi",
            True,
        ),
        (
            {"githost": "github", "pypi_support": "no"},
            [".github/workflows/release.yaml"],
            "pypi",
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
    cookies: plugin.Cookies,
) -> None:
    """Check for existence of text in files."""

    res = cookies.bake(extra_context=context)

    project_path = res.project_path
    for path in paths:
        text_exists = text in (project_path / path).read_text()
        assert text_exists == exist


def test_toml_blank_lines(baked_project: plugin.Result) -> None:
    """Check that TOML files do not have blank lines not followed by a [."""

    regex = re.compile(r"\n\s*\n[^[]")
    for path in file_matches(baked_project, r"^.*\.toml$"):
        text = path.read_text()
        match = regex.search(text)
        assert match is None, f"TOML file {path} contains blank lines."
