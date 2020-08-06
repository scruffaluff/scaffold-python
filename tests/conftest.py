"""Reusable testing fixtures."""


import pathlib

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
def baked_project(cookies: plugin.Cookies, request: SubRequest) -> pathlib.Path:
    """Cookiecutter projects baked from various parameters."""

    res = cookies.bake(extra_context=request.param)
    return pathlib.Path(res.project)
