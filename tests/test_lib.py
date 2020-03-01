"""General library testing."""


import pathlib

from pytest_cookies import plugin


def test_default(cookies: plugin.Cookies) -> None:
    """Check that default configuration generates correctly."""

    res = cookies.bake()

    assert res.exit_code == 0


def test_defaulr_removed_paths(cookies: plugin.Cookies) -> None:
    """Check that default configuration generates correctly."""

    res = cookies.bake()

    project_path = pathlib.Path(res.project)
    path_names = [path.name for path in project_path.iterdir()]
    assert ".gitlab-ci.yaml" not in path_names


def test_package_name_invalid(cookies: plugin.Cookies) -> None:
    """Check that cookiecutter rejects invalid package names."""

    res = cookies.bake(extra_context={"project_name": "$Mock?"})

    assert res.exit_code == -1
