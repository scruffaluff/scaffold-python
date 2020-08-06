"""Reusable testing fixtures."""


from _pytest.fixtures import SubRequest
import pytest
from pytest_cookies import plugin


@pytest.fixture(
    params=[
        {"cli_support": "no"},
        {"cli_support": "yes"},
        {"docker_support": "no"},
        {"docker_support": "yes"},
        {"githost": "github", "pypi_support": "yes"},
        {"githost": "github"},
        {"githost": "gitlab", "prettier_support": "no"},
        {"githost": "gitlab"},
        {"license": "MIT"},
        {"license": "private"},
        {"os": "linux"},
        {"os": "macos"},
        {"os": "windows"},
        {"prettier_support": "no"},
        {"prettier_support": "yes"},
        {"pypi_support": "no"},
        {"pypi_support": "yes"},
    ],
)
def baked_project(
    cookies: plugin.Cookies, request: SubRequest
) -> plugin.Result:
    """Cookiecutter projects baked from various parameters."""

    return cookies.bake(extra_context=request.param)
