#!/usr/bin/env sh
#
# Installs Tmate and creates a session suitable for CI pipelines. Based on logic
# from https://github.com/mxschmitt/action-tmate.

# Exit immediately if a command exits with non-zero return code.
#
# Flags:
#   -e: Exit immediately when a command fails.
#   -u: Throw an error when an unset variable is encountered.
set -eu

#######################################
# Show CLI help information.
# Cannot use function name help, since help is a pre-existing command.
# Outputs:
#   Writes help information to stdout.
#######################################
usage() {
  case "${1}" in
    main)
      cat 1>&2 << EOF
Installs Tmate and creates a remote session. Users can close the session by
creating the file /close-tmate.

Usage: setup-tmate [OPTIONS]

Options:
      --debug     Show shell debug traces
  -h, --help      Print help information
  -v, --version   Print version information
EOF
      ;;
    *)
      error "No such usage option '${1}'"
      ;;
  esac
}

#######################################
# Assert that command can be found in system path.
# Will exit script with an error code if command is not in system path.
# Arguments:
#   Command to check availabilty.
# Outputs:
#   Writes error message to stderr if command is not in system path.
#######################################
assert_cmd() {
  # Flags:
  #   -v: Only show file path of command.
  #   -x: Check if file exists and execute permission is granted.
  if [ ! -x "$(command -v "${1}")" ]; then
    error "Cannot find required ${1} command on computer"
  fi
}

#######################################
# Print error message and exit script with error code.
# Outputs:
#   Writes error message to stderr.
#######################################
error() {
  bold_red='\033[1;31m' default='\033[0m'
  printf "${bold_red}error${default}: %s\n" "${1}" >&2
  exit 1
}

#######################################
# Install Tmate.
# Arguments:
#   Whether to use sudo command.
#######################################
install_tmate() {
  assert_cmd uname

  # Do not use long form --kernel-name flag for uname. It is not supported on
  # MacOS.
  os_type="$(uname -s)"
  case "${os_type}" in
    Darwin)
      # Setting environment variable 'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK'
      # prevents upgrading outdated system packages during a Homebrew
      # installation of a new package. This is necessary since in some systems,
      # such as GitLab CI, upgrading system packages causes breakage.
      HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK='true' brew install tmate
      ;;
    FreeBSD)
      ${1:+sudo} pkg update
      ${1:+sudo} pkg install --yes tmate
      ;;
    Linux)
      install_tmate_linux "${1}"
      ;;
    *)
      error "Operating system ${os_type} is not supported"
      ;;
  esac
}

#######################################
# Install Tmate for Linux.
# Arguments:
#   Whether to use sudo command.
#######################################
install_tmate_linux() {
  tmate_version='2.4.0'

  # Short form machine flag '-m' should be used since processor flag and long
  # form machine flag '--machine' are non-portable. For more information, visit
  # https://www.gnu.org/software/coreutils/manual/html_node/uname-invocation.html#index-_002dp-12.
  arch_type="$(uname -m)"
  case "${arch_type}" in
    x86_64 | amd64)
      tmate_arch='amd64'
      ;;
    arm64 | aarch64)
      tmate_arch='arm64v8'
      ;;
    *)
      error "Unsupported architecture ${arch_type}"
      ;;
  esac

  # Install OpenSSH and archive utils.
  #
  # Flags:
  #   -v: Only show file path of command.
  #   -x: Check if file exists and execute permission is granted.
  if [ -x "$(command -v apk)" ]; then
    ${1:+sudo} apk add curl openssh-client xz
  elif [ -x "$(command -v apt-get)" ]; then
    ${1:+sudo} apt-get update
    ${1:+sudo} apt-get install --yes curl openssh-client xz-utils
  elif [ -x "$(command -v dnf)" ]; then
    ${1:+sudo} dnf install --assumeyes curl openssh xz
  elif [ -x "$(command -v pacman)" ]; then
    ${1:+sudo} pacman --noconfirm --refresh --sync --sysupgrade
    ${1:+sudo} pacman --noconfirm --sync curl openssh xz
  elif [ -x "$(command -v zypper)" ]; then
    ${1:+sudo} zypper install --no-confirm curl openssh tar xz
  fi

  curl -LSfs "https://github.com/tmate-io/tmate/releases/download/${tmate_version}/tmate-${tmate_version}-static-linux-${tmate_arch}.tar.xz" -o /tmp/tmate.tar.xz
  tar xvf /tmp/tmate.tar.xz --directory /tmp --strip-components 1
  ${1:+sudo} install /tmp/tmate /usr/local/bin/tmate
  rm /tmp/tmate /tmp/tmate.tar.xz
}

#######################################
# Installs Tmate and creates a remote session.
#######################################
setup_tmate() {
  # Use sudo for system installation if user is not root. Do not use long form
  # --user flag for id. It is not supported on MacOS.
  if [ "$(id -u)" -ne 0 ]; then
    assert_cmd sudo
    use_sudo='true'
  else
    use_sudo=''
  fi

  # Install Tmate if not available.
  #
  # Flags:
  #   -v: Only show file path of command.
  #   -x: Check if file exists and execute permission is granted.
  if [ ! -x "$(command -v tmate)" ]; then
    install_tmate "${use_sudo}"
  fi

  # Launch new Tmate session with custom socket.
  #
  # Flags:
  #   -S: Set Tmate socket path.
  tmate -S /tmp/tmate.sock new-session -d
  tmate -S /tmp/tmate.sock wait tmate-ready
  ssh_connect="$(tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}')"
  web_connect="$(tmate -S /tmp/tmate.sock display -p '#{tmate_web}')"

  while true; do
    echo "SSH: ${ssh_connect}"
    echo "Web shell: ${web_connect}"

    # Check if script should exit.
    #
    # Flags:
    #   -S: Check if file exists and is a socket.
    #   -f: Check if file exists and is a regular file.
    if [ ! -S /tmp/tmate.sock ] || [ -f /close-tmate ] || [ -f ./close-tmate ]; then
      break
    fi

    sleep 5
  done
}

#######################################
# Print Setup Tmate version string.
# Outputs:
#   Setup Tmate version string.
#######################################
version() {
  echo 'SetupTmate 0.2.1'
}

#######################################
# Script entrypoint.
#######################################
main() {
  # Parse command line arguments.
  while [ "${#}" -gt 0 ]; do
    case "${1}" in
      --debug)
        set -o xtrace
        shift 1
        ;;
      -h | --help)
        usage 'main'
        exit 0
        ;;
      -v | --version)
        version
        exit 0
        ;;
      *) ;;
    esac
  done

  setup_tmate
}

main "$@"
