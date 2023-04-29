<#
.SYNOPSIS
    Installs Tmate and creates a session suitable for CI. Based on logic from
    https://github.com/mxschmitt/action-tmate.
#>
[CmdletBinding()]
Param()

# Exit immediately if a PowerShell Cmdlet encounters an error.
$ErrorActionPreference = 'Stop'

Function InstallTmate($URL) {
    If (-Not (Get-Command choco -ErrorAction SilentlyContinue)) {
        RemoteScript 'https://chocolatey.org/install.ps1'
    }

    If (-Not (Get-Command pacman -ErrorAction SilentlyContinue)) {
        choco install --yes msys2
    }

    pacman --noconfirm --sync tmate
}

# Request remote script and execution efficiently.
#
# Required as a seperate function, since the default progress bar updates every
# byte, making downloads slow. For more information, visit
# https://stackoverflow.com/a/43477248.
Function RemoteScript($URL) {
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -UseBasicParsing -Uri "$URL" | Invoke-Expression
}

# Script entrypoint.
Function Main() {
    $Env:Path = 'C:\tools\msys64\usr\bin;' + $Env:Path
    If (-Not (Get-Command tmate -ErrorAction SilentlyContinue)) {
        InstallTmate
    }

    # Set Msys2 environment variables.
    $Env:CHERE_INVOKING = 1
    $Env:MSYS2_PATH_TYPE = 'inherit'
    $Env:MSYSTEM = 'MINGW64'

    # Launch new Tmate session with custom socket.
    #
    # Flags:
    #   -S: Set Tmate socket path.
    tmate -S /tmp/tmate.sock new-session -d
    tmate -S /tmp/tmate.sock wait tmate-ready
    $SSHConnect = "$(bash -l -c "tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'")"
    $WebConnect = "$(bash -l -c "tmate -S /tmp/tmate.sock display -p '#{tmate_web}'")"

    While ($True) {
        Write-Output "SSH: $SSHConnect"
        Write-Output "Web shell: $WebConnect"

        # Check if script should exit.
        If (
            (-Not (bash -l -c "ls /tmp/tmate.sock 2> /dev/null")) -Or 
            (Test-Path -Path 'C:/tools/msys64/close-tmate') -Or 
            (Test-Path -Path './close-tmate')
        ) {
            Break
        }

        Sleep 5
    }
}

# Only run Main if invoked as script. Otherwise import functions as library.
If ($MyInvocation.InvocationName -NE '.') {
    Main $Args
}
