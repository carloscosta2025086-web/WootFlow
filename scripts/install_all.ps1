param(
    [switch]$SkipUi
)

$ErrorActionPreference = "Stop"

function Require-Command {
    param([string]$Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Comando '$Name' nao encontrado no PATH."
    }
}

Write-Host "[1/5] Verificar pre-requisitos..." -ForegroundColor Cyan
Require-Command -Name python
Require-Command -Name npm

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "[2/5] Criar/validar ambiente virtual Python..." -ForegroundColor Cyan
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao criar ambiente virtual Python."
    }
}

Write-Host "[3/5] Instalar dependencias Python..." -ForegroundColor Cyan
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao atualizar pip."
}

& ".\.venv\Scripts\python.exe" -m pip install -r requirements_screen_ambience.txt
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao instalar dependencias Python."
}

if (-not $SkipUi) {
    Write-Host "[4/5] Instalar dependencias da UI (npm ci)..." -ForegroundColor Cyan
    if (-not (Test-Path "ui\package-lock.json")) {
        throw "ui/package-lock.json nao encontrado."
    }

    Push-Location "ui"
    npm ci
    if ($LASTEXITCODE -ne 0) {
        Pop-Location
        throw "Falha ao instalar dependencias da UI (npm ci)."
    }
    Pop-Location
} else {
    Write-Host "[4/5] UI ignorada por parametro -SkipUi." -ForegroundColor Yellow
}

Write-Host "[5/5] Concluido." -ForegroundColor Green
Write-Host "Para executar a app: .\.venv\Scripts\python.exe main_desktop.py" -ForegroundColor Green
