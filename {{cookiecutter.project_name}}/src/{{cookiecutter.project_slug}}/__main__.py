"""Command line interface for {{ cookiecutter.project_name }}.

See https://docs.python.org/3/using/cmdline.html#cmdoption-m for why module is
named __main__.py.
"""

import sys
from typing import Annotated, Optional

from typer import Option, Typer

import {{ cookiecutter.project_slug }}


cli = Typer(
    add_completion=False,
    help="{{ cookiecutter.project_description }}",
    pretty_exceptions_enable=False,
)


def print_version(value: bool) -> None:
    """Print {{ cookiecutter.project_name }} version string."""
    if value:
        print(f"{{ cookiecutter.project_name }} {{ '{' }}{{ cookiecutter.project_slug }}.__version__{{ '}' }}")
        sys.exit()


@cli.command()
def main(
    version: Annotated[
        Optional[bool],
        Option(
            "-v",
            "--version",
            callback=print_version,
            help="Print version information",
            is_eager=True,
        ),
    ] = False,
) -> None:
    pass


if __name__ == "__main__":
    cli()
