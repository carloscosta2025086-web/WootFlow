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

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "[2/5] Criar/validar ambiente virtual Python..." -ForegroundColor Cyan
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
}

Write-Host "[3/5] Instalar dependencias Python..." -ForegroundColor Cyan
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements_screen_ambience.txt

if (-not $SkipUi) {
    Write-Host "[4/5] Instalar dependencias da UI (npm ci)..." -ForegroundColor Cyan
    if (-not (Test-Path "ui\package-lock.json")) {
        throw "ui/package-lock.json nao encontrado."
    }

    Push-Location "ui"
    npm ci
    Pop-Location
} else {
    Write-Host "[4/5] UI ignorada por parametro -SkipUi." -ForegroundColor Yellow
}

Write-Host "[5/5] Concluido." -ForegroundColor Green
Write-Host "Para executar a app: .\.venv\Scripts\python.exe main_desktop.py" -ForegroundColor Green
