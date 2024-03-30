"""Command line interface for {{ cookiecutter.project_name }}.

See https://docs.python.org/3/using/cmdline.html#cmdoption-m for why module is
named __main__.py.
"""

from typer import Typer


app = Typer(help="{{ cookiecutter.project_description }}")


if __name__ == "__main__":
    app()
