"""Reusable testing fixtures."""

from _pytest.fixtures import SubRequest
import pytest
from pytest_cookies.plugin import Cookies, Result


@pytest.fixture(
    params=[
        {"cli_support": "no"},
        {"cli_support": "yes"},
        {"githost": "github", "pypi_support": "yes"},
        {"githost": "github"},
        {"githost": "gitlab", "prettier_support": "no"},
        {"githost": "gitlab"},
        {"license": "MIT"},
        {"license": "private"},
        {"prettier_support": "no"},
        {"prettier_support": "yes"},
        {"pypi_support": "no"},
        {"pypi_support": "yes"},
    ],
)
def baked_project(cookies: Cookies, request: SubRequest) -> Result:
    """Cookiecutter projects baked from various parameters."""
    return cookies.bake(extra_context=request.param)
