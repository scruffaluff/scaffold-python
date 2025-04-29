# Just configuration file for running commands.
#
# For more information, visit https://just.systems.

set script-interpreter := ["nu"]
set shell := ["nu", "--commands"]
set unstable := true
set windows-shell := ["nu", "--commands"]
export PATH := if os() == "windows" {
  justfile_dir() / ".vendor/bin;" + env_var("Path")
} else {
  justfile_dir() / ".vendor/bin:" + env_var("PATH")
}

# List all commands available in justfile.
list:
  just --list

# Execute CI workflow commands.
ci: setup lint doc test

# Build documentation.
[script]
doc:
  mkdir docs
  cp README.md docs/index.md
  uv run mkdocs build --strict

# Fix code formatting.
format:
  prettier --write .
  uv run black --write .

# Run code analyses.
lint:
  uv run flake8 .
  uv run mypy .

# Install development dependencies.
[script]
setup: _setup
  uv sync

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
      iex "& { $(iwr -useb https://scruffaluff.github.io/scripts/install/uv.ps1) } --preserve-env --dest .vendor/bin"
    }
  }
  uv --version

# Run test suites.
test:
  uv run pytest
