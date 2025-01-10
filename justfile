# Just configuration file for running commands.
#
# For more information, visit https://just.systems.

set windows-shell := ['pwsh.exe', '-NoLogo', '-Command']

# List all commands available in justfile.
list:
  just --list

# Execute all development commands.
all: setup format lint docs test

# Build documentation.
docs: _docs_mkdir
  cp README.md docs/index.md
  poetry run mkdocs build --strict

[unix]
_docs_mkdir:
  mkdir -p docs

[windows]
_docs_mkdir:
  New-Item -Force -ItemType Directory docs

# Check code formatting.
format:
  prettier --check .
  poetry run black --check .

# Run code analyses.
lint:
  poetry run flake8 .
  poetry run mypy .

# Install development dependencies.
setup:
  node --version
  npm --version
  npm install --global prettier
  python3 --version
  python3 -m venv .venv
  python3 -m pip --version
  poetry --version
  poetry check --lock
  poetry install

# Run test suites.
test:
  poetry run pytest
