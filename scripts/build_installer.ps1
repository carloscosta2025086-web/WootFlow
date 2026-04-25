param(
    [string]$Version = "0.0.0-local",
    [switch]$SkipUiBuild,
    [switch]$SkipExeBuild,
    [switch]$DownloadPrereqs,
    [string]$WebView2StandaloneUrl = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if ($DownloadPrereqs) {
    $downloadArgs = @{}
    if ($WebView2StandaloneUrl) {
        $downloadArgs.WebView2StandaloneUrl = $WebView2StandaloneUrl
    }
    & (Join-Path $repoRoot "scripts\download_installer_prereqs.ps1") @downloadArgs
}

if (-not $SkipUiBuild) {
    Write-Host "[1/4] Build UI" -ForegroundColor Cyan
    Push-Location (Join-Path $repoRoot "ui")
    npm ci
    if ($LASTEXITCODE -ne 0) { throw "Falha em npm ci" }
    npm run build
    if ($LASTEXITCODE -ne 0) { throw "Falha em npm run build" }
    Pop-Location
}

$appVersionFile = Join-Path $repoRoot "app_version.py"
Set-Content -Path $appVersionFile -Value ("APP_VERSION = `"{0}`"" -f $Version)

if (-not $SkipExeBuild) {
    Write-Host "[2/4] Build EXE" -ForegroundColor Cyan
    & ".\.venv\Scripts\python.exe" -m pip install pyinstaller
    if ($LASTEXITCODE -ne 0) { throw "Falha ao instalar PyInstaller" }
    & ".\.venv\Scripts\python.exe" -m PyInstaller WootingRGB.spec --clean -y
    if ($LASTEXITCODE -ne 0) { throw "Falha ao gerar EXE" }
}

Write-Host "[3/4] Localizar Inno Setup Compiler" -ForegroundColor Cyan
$iscc = (Get-Command iscc.exe -ErrorAction SilentlyContinue).Source
if (-not $iscc) {
    $candidate = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if (Test-Path $candidate) {
        $iscc = $candidate
    }
}
if (-not $iscc) {
    throw "ISCC.exe nao encontrado. Instala Inno Setup 6 ou adiciona iscc.exe ao PATH."
}

$distDir = Join-Path $repoRoot "dist"
if (-not (Test-Path (Join-Path $distDir "WootingRGB.exe"))) {
    throw "dist\WootingRGB.exe nao encontrado."
}

Write-Host "[4/4] Compilar instalador" -ForegroundColor Cyan
& $iscc "/DAppVersion=$Version" "/DRepoDir=$repoRoot" "/DSourceDir=$distDir" (Join-Path $repoRoot "installer\WootFlowInstaller.iss")
if ($LASTEXITCODE -ne 0) { throw "Falha ao compilar instalador Inno Setup" }

Write-Host "Instalador gerado em installer\output" -ForegroundColor Green
