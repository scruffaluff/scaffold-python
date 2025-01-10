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
docs: _docs-index
  poetry run mkdocs build --strict

[unix]
_docs-index:
  mkdir -p docs
  cp README.md docs/index.md

[windows]
_docs-index:
  New-Item -Force -ItemType Container docs
  Copy-Item -Force README.md docs/index.md

# Check code formatting.
format:
  prettier --check .
  poetry run black --check .

# Run code analyses.
lint:
  poetry run flake8 .
  poetry run mypy .

# Install development dependencies.
setup: _setup
  prettier --version
  python3 --version
  python3 -m venv .venv
  python3 -m pip --version
  poetry --version
  poetry check --lock
  poetry install

[unix]
_setup:
  #!/usr/bin/env sh
  set -eu
  if [ "$(id -u)" -eq 0 ]; then
    super=''
  elif [ -x "$(command -v sudo)" ]; then
    super='sudo'
  elif [ -x "$(command -v doas)" ]; then
    super='doas'
  fi
  if [ ! -x "$(command -v prettier)" ]; then
    if [ -x "$(command -v npm)" ]; then
      npm install --global prettier
    elif [ -x "$(command -v apk)" ]; then
      ${super:+"${super}"} apk update
      ${super:+"${super}"} apk add nodejs npm
      npm install --global prettier
    elif [ -x "$(command -v apt-get)" ]; then
      ${super:+"${super}"} apt-get update
      ${super:+"${super}"} apt-get install --yes nodejs npm
      npm install --global prettier
    elif [ -x "$(command -v brew)" ]; then
      brew install node
      npm install --global prettier
    elif [ -x "$(command -v dnf)" ]; then
      ${super:+"${super}"} dnf check-update || {
        code="$?"
        [ "${code}" -ne 100 ] && exit "${code}"
      }
      ${super:+"${super}"} dnf install --assumeyes nodejs nodejs-npm
      npm install --global prettier
    elif [ -x "$(command -v pacman)" ]; then
      ${super:+"${super}"} pacman --noconfirm --refresh --sync --sysupgrade
      ${super:+"${super}"} pacman --noconfirm --sync nodejs npm
      npm install --global prettier
    elif [ -x "$(command -v pkg)" ]; then
      ${super:+"${super}"} pkg update
      ${super:+"${super}"} pkg install --yes node npm-node
      npm install --global prettier
    else
      echo 'Error: No supported package manager to install Prettier.' >&2
      echo 'Please install Prettier manually before continuing.' >&2
      exit 1
    fi
  fi
   if [ ! -x "$(command -v python)" ]; then
    if [ -x "$(command -v apk)" ]; then
      ${super:+"${super}"} apk update
      ${super:+"${super}"} apk add py3-pip python3 python3-dev
    elif [ -x "$(command -v apt-get)" ]; then
      ${super:+"${super}"} apt-get update
      ${super:+"${super}"} apt-get install --yes python3 python3-dev python3-pip python3-venv
    elif [ -x "$(command -v brew)" ]; then
      brew install python
    elif [ -x "$(command -v dnf)" ]; then
      ${super:+"${super}"} dnf check-update || {
        code="$?"
        [ "${code}" -ne 100 ] && exit "${code}"
      }
      ${super:+"${super}"} dnf install --assumeyes python3 python3-devel python3-pip
    elif [ -x "$(command -v pacman)" ]; then
      ${super:+"${super}"} pacman --noconfirm --refresh --sync --sysupgrade
      ${super:+"${super}"} pacman --noconfirm --sync python python-pip
    elif [ -x "$(command -v pkg)" ]; then
      ${super:+"${super}"} pkg update
      ${super:+"${super}"} pkg install --yes py311-pip python3
    else
      echo 'Error: No supported package manager to install Python.' >&2
      echo 'Please install Python manually before continuing.' >&2
      exit 1
    fi
  fi
  if [ ! -x "$(command -v poetry)" ]; then
    python3 -m pip install --user poetry poetry-plugin-shell
  fi

[windows]
_setup:
  #!powershell.exe
  $ErrorActionPreference = 'Stop'
  If (-Not (Get-Command -ErrorAction SilentlyContinue prettier)) {
    If (Get-Command -ErrorAction SilentlyContinue npm) {
      npm install --global prettier
    }
    ElseIf (Get-Command -ErrorAction SilentlyContinue choco) {
      choco install --yes nodejs
      npm install --global prettier
    }
    ElseIf (Get-Command -ErrorAction SilentlyContinue scoop) {
      scoop install nodejs
      npm install --global prettier
    }
    ElseIf (Get-Command -ErrorAction SilentlyContinue winget) {
      winget install --disable-interactivity --exact --id openjs.nodejs
      npm install --global prettier
    } 
    Else {
      Write-Error 'Error: No supported package manager to install Prettier.'
      Write-Error 'Please install Prettier manually before continuing.'
      Exit 1
    }
  }
  If (-Not (Get-Command -ErrorAction SilentlyContinue python3)) {
    If (Get-Command -ErrorAction SilentlyContinue choco) {
      choco install --yes python3
    }
    ElseIf (Get-Command -ErrorAction SilentlyContinue scoop) {
      scoop install python
    }
    ElseIf (Get-Command -ErrorAction SilentlyContinue winget) {
      winget install --disable-interactivity --exact --id python.python.3.12
    } 
    Else {
      Write-Error 'Error: No supported package manager to install Python.'
      Write-Error 'Please install Python manually before continuing.'
      Exit 1
    }
  }
  If (-Not (Get-Command -ErrorAction SilentlyContinue poetry)) {
    python3 -m pip install --user poetry poetry-plugin-shell
  }

# Run test suites.
test:
  poetry run pytest
