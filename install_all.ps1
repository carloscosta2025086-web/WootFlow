param(
    [switch]$SkipUi
)

# Backward-compatible wrapper: keeps old command working from repo root.
$scriptPath = Join-Path $PSScriptRoot "scripts\install_all.ps1"
if (-not (Test-Path $scriptPath)) {
    throw "Nao foi encontrado: $scriptPath"
}

& $scriptPath @PSBoundParameters
