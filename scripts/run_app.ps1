param(
    [switch]$SkipUiBuild,
    [switch]$SkipUiDeps,
    [switch]$ForceUiBuild
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "[1/4] Verificar e instalar dependencias" -ForegroundColor Cyan
$installArgs = @{}
if ($SkipUiDeps) {
    $installArgs.SkipUi = $true
}
& (Join-Path $repoRoot "scripts\install_all.ps1") @installArgs

if (-not $SkipUiBuild) {
    $uiDistIndex = Join-Path $repoRoot "ui\dist\index.html"
    $needsBuild = $ForceUiBuild -or (-not (Test-Path $uiDistIndex))

    if ($needsBuild) {
        Write-Host "[2/4] Build da UI" -ForegroundColor Cyan
        Push-Location (Join-Path $repoRoot "ui")
        npm run build
        if ($LASTEXITCODE -ne 0) {
            Pop-Location
            throw "Falha em npm run build"
        }
        Pop-Location
    }
    else {
        Write-Host "[2/4] UI build ja existe (ui/dist)." -ForegroundColor Green
    }
}
else {
    Write-Host "[2/4] Build UI ignorado por parametro -SkipUiBuild" -ForegroundColor Yellow
}

Write-Host "[3/4] Validar runtime e arrancar app" -ForegroundColor Cyan
Write-Host "      (main_desktop.py faz verificacao de WebView2/VC++ no arranque)" -ForegroundColor DarkCyan

Write-Host "[4/4] Abrir WootFlow" -ForegroundColor Green
& ".\.venv\Scripts\python.exe" "main_desktop.py"
