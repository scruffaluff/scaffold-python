# Scaffold Python

![](https://github.com/wolfgangwazzlestrauss/scaffold-python/workflows/build/badge.svg)
![](https://img.shields.io/badge/code%20style-black-000000.svg)
![](https://img.shields.io/github/repo-size/wolfgangwazzlestrauss/scaffold-python)
![](https://img.shields.io/github/license/wolfgangwazzlestrauss/scaffold-python)

---

**Documentation**: https://wolfgangwazzlestrauss.github.io/scaffold-python

**Source Code**: https://github.com/wolfgangwazzlestrauss/scaffold-python

---

Scaffold Python is a
[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template project
for generating Python repository layouts. To create a new Python application
project with the template first install
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
black .
git init
```

Then the development environment is configured and you are ready to code.

## Tooling

Every generated project configures the following tools for development usage:

- [Bandit](https://github.com/PyCQA/bandit): Security linter.
- [Black](https://github.com/psf/black): Opinionated code formatter.
- [Coverage](https://coverage.readthedocs.io/en/coverage-5.0.3/): Test coverage
  measurer.
- [Flake8](https://flake8.pycqa.org/en/latest/): Code linter.
  - [Flake8 Bugbear](https://github.com/PyCQA/flake8-bugbear): Flake8 plugin for
    finding bugs and design problems.
  - [Flake8 Docstrings](https://gitlab.com/pycqa/flake8-docstrings): Flake8
    plugin for checking docstring styles.
  - [Flake8 Import Order](https://github.com/PyCQA/flake8-import-order): Flake8
    plugin for checking module import orders.
- [MkDocs](https://www.mkdocs.org/): Documentation static site generator.
- [Mypy](http://mypy-lang.org/): Static type checker.
- [Poetry](https://python-poetry.org/): Dependency manager and packager.
- [Pytest](https://docs.pytest.org/en/latest/): Testing framework.
- [Tox](https://tox.readthedocs.io/en/latest/): Test automator.

The following tools are configured if you select optional features:

- `prettier_support`:
  - [Prettier](https://prettier.io/): Opinionated code formatter for JSON,
    Markdown, and YAML files. Requires [NodeJS](https://nodejs.org/en/) to be
    externally installed on your system.

## Layout

The following diagram shows all possible files generated from scaffolding. If a
file is followed by `{option: selection}`, then the path and its possible
subcontents are only generated for that chosen context.

```
{{project_name}}
├── .dockerignore
├── docs
|   ├── api
│   |   └── index.md
|   ├── contrib
│   |   └── index.md
│   ├── css
│   │   └── mkdocstrings.css
│   ├── install
│   │   └── index.md
│   └── learn
│       └── index.md
├── examples
│   └── __init__.py
├── .github  {githost: github}
│   └── workflows
│       ├── build.yaml
│       ├── package.yaml
│       └── pages.yaml
├── .gitignore
├── LICENSE.md
├── mkdocs.yml
├── mypy.ini
├── package.json  {prettier_support: yes}
├── .prettierignore  {prettier_support: yes}
├── pyproject.toml
├── README.md
├── scripts
|   ├── __init__.py
│   └── build_docs.py
├── src
│   └── {{project_slug}}
│       ├── __init__.py
|       ├── __main__.py  {cli_support: yes}
│       └── py.typed
├── tests
│   ├── conftest.py
│   ├── __init__.py
│   ├── integration
│   │   └── __init__.py
│   └── unit
│       └── __init__.py
└── tox.ini
```

## Continous Integration

Projects generated with this scaffolding repository come with configured
pipeline for GitHub CI workflows and GitLab CI pipelines.

### Linting and Testing

### Documentation Publishing

### Package Publishing
