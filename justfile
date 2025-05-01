# Just configuration file for running commands.
#
# For more information, visit https://just.systems.

set script-interpreter := ["nu"]
set shell := ["nu", "--commands"]
set unstable := true
set windows-shell := ["nu", "--commands"]
export PATH := if os() == "windows" {
  justfile_dir() / ".vendor/bin;" + env_var("PATH")
} else {
  justfile_dir() / ".vendor/bin:" + env_var("PATH")
}

# List all commands available in justfile.
list:
  just --list

# Execute CI workflow commands.
ci: setup lint doc test-ver

# Build documentation.
[script]
doc:
  mkdir doc
  cp README.md doc/index.md
  uv run mkdocs build --strict

# Fix code formatting.
format:
  deno run --allow-all npm:prettier --write .
  # uv run ruff format .
  uv run black --write .

# Run code analyses.
lint:
  deno run --allow-all npm:prettier --check .
  # uv run ruff check .
  uv run flake8 .
  uv run mypy .

# Install development dependencies.
setup: _setup
  uv sync --locked

[unix]
_setup:
  #!/usr/bin/env sh
  set -eu
  if [ ! -x "$(command -v nu)" ]; then
    curl --fail --location --show-error \
      https://scruffaluff.github.io/scripts/install/nushell.sh | sh -s -- \
      --preserve-env --dest .vendor/bin
  fi
  echo "Nushell $(nu --version)"
  if [ ! -x "$(command -v deno)" ]; then
    curl --fail --location --show-error \
      https://scruffaluff.github.io/scripts/install/deno.sh | sh -s -- \
      --preserve-env --dest .vendor/bin
  fi
  deno --version
  if [ ! -x "$(command -v uv)" ]; then
    curl --fail --location --show-error \
      https://scruffaluff.github.io/scripts/install/uv.sh | sh -s -- \
      --preserve-env --dest .vendor/bin
  fi
  uv --version

[windows]
_setup:
  #!powershell.exe
  $ErrorActionPreference = 'Stop'
  $ProgressPreference = 'SilentlyContinue'
  $PSNativeCommandUseErrorActionPreference = $True
  if (-not (Get-Command -ErrorAction SilentlyContinue nu)) {
    powershell {
      iex "& { $(iwr -useb https://scruffaluff.github.io/scripts/install/nushell.ps1) } --preserve-env --dest .vendor/bin"
    }
  }
  Write-Output "Nushell $(nu --version)"
  if (-not (Get-Command -ErrorAction SilentlyContinue deno)) {
    powershell {
      iex "& { $(iwr -useb https://scruffaluff.github.io/scripts/install/deno.ps1) } --preserve-env --dest .vendor/bin"
    }
  }
  deno --version
  if (-not (Get-Command -ErrorAction SilentlyContinue uv)) {
    powershell {
      iex "& { $(iwr -useb https://scruffaluff.github.io/scripts/install/uv.ps1) } --preserve-env --dest .vendor/bin"
    }
  }
  uv --version

# Run test suites.
test *args:
  uv run pytest {{args}}

# Run test suite for multiple Python versions.
[script]
test-ver versions="3.9,3.10,3.11,3.12,3.13":
  let versions = "{{versions}}" | split row ","
  for version in $versions { uv run --python $version pytest }
