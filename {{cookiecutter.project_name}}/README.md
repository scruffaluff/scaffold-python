# {{ cookiecutter.project_name }}

---

**Documentation**: {{ cookiecutter.project_homepage }}

**Source Code**: {{ cookiecutter.project_repository }}

---

{{ cookiecutter.project_name }}

## Getting Started

### Installation

{{ cookiecutter.project_name }} can be installed for Python 3.9+ with

```bash
pip install --user {{ cookiecutter.project_slug }}
```

## Contributing

For guidance on setting up a development environment and making a contribution
to {{cookiecutter.project_name }}, see the [contributing guide](CONTRIBUTING.md).

## License

{% if cookiecutter.license != "private" -%}
Distributed under the terms of the [{{ cookiecutter.license }} license](LICENSE.md), {{
cookiecutter.project_name }} is
free and open source software.
{% else -%}
{{ cookiecutter.project_name }} is proprietary software and prohibited from unauthorized
redistribution. See the [license](LICENSE.md) for more information.
{% endif -%}
