"""General library testing."""


from pytest_cookies import plugin


def test_default(cookies: plugin.Cookies) -> None:
    """Check that default configuration generates correctly."""

    res = cookies.bake()

    assert res.exit_code == 0


def test_package_name_invalid(cookies: plugin.Cookies) -> None:
    """Check that cookiecutter rejects invalid package names."""

    res = cookies.bake(extra_context={"project_name": "$Mock?"})

    assert res.exit_code == -1
