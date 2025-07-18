# Scaffold Python

![](https://img.shields.io/github/repo-size/scruffaluff/scaffold-python)
![](https://img.shields.io/github/license/scruffaluff/scaffold-python)

Scaffold Python is a
[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template project
for generating Python repository layouts. To create a new Python application
project with the template first install
[Cookiecutter](https://github.com/cookiecutter/cookiecutter). Then execute

```console
cookiecutter https://github.com/scruffaluff/scaffold-python
```

Follow the interactive prompts, and a folder, with your selected `project_name`,
will be generated in your current working directory.

## Setup

To develop with the generated project, install [Just](https://just.systems) and
step into the project folder. Then execute `just init` and you are ready to
code.

## Tooling

Every generated project configures the following tools for development usage:

- [Coverage](https://coverage.readthedocs.io/en/coverage-5.0.3/): Test coverage
  measurer.
- [MkDocs](https://www.mkdocs.org/): Documentation static site generator.
- [Mypy](http://mypy-lang.org/): Static type checker.
- [Ruff](https://docs.astral.sh/ruff/): Code linter.
- [Pytest](https://docs.pytest.org/en/latest/): Testing framework.
- [Tox](https://tox.readthedocs.io/en/latest/): Test automator.
- [Uv](https://docs.astral.sh/uv/): Dependency manager and packager.

The following tools are configured if you select optional features:

- `prettier_support`:
  - [Prettier](https://prettier.io/): Opinionated code formatter for JSON,
    Markdown, and YAML files. Requires [NodeJS](https://nodejs.org/en/) to be
    externally installed on your system.

## Layout

The following diagram shows all possible files generated from scaffolding. If a
file is followed by `{option: selection}`, then the path and its possible
contents are only generated for that chosen context.

```
{{project_name}}
├── .github  {githost: github}
│   └── workflows
│       └── main.yaml
├── .dockerignore
├── .gitignore
├── .gitlab-ci.yaml  {githost: gitlab}
├── .prettierignore  {prettier_support: yes}
├── .prettierrc.yaml  {prettier_support: yes}
├── CONTRIBUTING.md
├── doc
│   ├── api
│   |   └── index.md
│   └── usage
│       └── index.md
├── LICENSE.md
├── mkdocs.yml
├── pyproject.toml
├── README.md
├── src
│   └── {{project_slug}}
│       ├── __init__.py
│       ├── __main__.py  {cli_support: yes}
│       └── py.typed
├── test
│   ├── conftest.py
│   └── __init__.py
└── tox.ini
```

## Continuous Integration

Projects generated with this scaffolding repository are automatically configured
to use GitHub CI workflows and GitLab CI pipelines.
