# scaffold-python

Scaffold Python is a
[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template project
for generating Python application repository layouts. To create a new Python
application project with the template first install
[Cookiecutter](https://github.com/cookiecutter/cookiecutter). Then execute

```console
cookiecutter https://github.com/wolfgangwazzlestrauss/scaffold-python
```

Follow the interactive prompts, and a folder, with your selected `project_name`,
will be generated in your current working directory.


## Setup

To develop with the generated project, install
[Poetry](https://python-poetry.org/) and step into the project folder.
Afterwards execute:

```console
poetry install
poetry shell
git init
pre-commit install
```

Then the development environment is configured and you are ready to code.

## Tooling

The generated project configures the following tools for development usage:

* [Bandit](https://github.com/PyCQA/bandit): Security linter.
* [Black](https://github.com/psf/black): Opinionated code formatter.
* [Coverage](https://coverage.readthedocs.io/en/coverage-5.0.3/): Test coverage
  measurer.
* [Flake8](https://flake8.pycqa.org/en/latest/): Code linter.
* [Mypy](http://mypy-lang.org/): Static type checker.
* [Poetry](https://python-poetry.org/): Dependency manager and packager.
* [Pre-Commit](https://pre-commit.com/): Git pre-commit hooks manager.
* [Pytest](https://docs.pytest.org/en/latest/): Testing framework.
* [Tox](https://tox.readthedocs.io/en/latest/): Test automator.

## Layout

The generated project structure is as follows:

```
{{project_name}}
├── CONTRIBUTING.md
├── docs
├── .github
│   └── workflows
│       ├── build.yaml
│       └── publish.yaml
├── .gitignore
├── .gitlab-ci.yaml
├── LICENSE.md
├── mypy.ini
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
├── src
│   └── {{project_slug}}
│       ├── __init__.py
│       └── py.typed
├── tests
│   ├── conftest.py
│   ├── __init__.py
│   ├── integration
│   │   └── __init__.py
│   └── unit
│       ├── __init__.py
│       └── test_lib.py
└── tox.ini
```

Some of the files or directories may not be generated based on your chosen
options.
