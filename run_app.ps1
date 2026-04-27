param(
    [switch]$SkipUiBuild,
    [switch]$SkipUiDeps,
    [switch]$ForceUiBuild
)

# Backward-compatible wrapper from repo root.
$scriptPath = Join-Path $PSScriptRoot "scripts\run_app.ps1"
if (-not (Test-Path $scriptPath)) {
    throw "Nao foi encontrado: $scriptPath"
}

& $scriptPath @PSBoundParameters
