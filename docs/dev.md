# Desenvolvimento (sem rebuild de EXE)

## Objetivo
Fluxo rapido para alterar, testar e depurar sem gerar `.exe` em cada mudanca.

## Setup inicial
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_all.ps1
```

## Backend + desktop local
```powershell
.\.venv\Scripts\python.exe main_desktop.py
```

## Backend isolado
```powershell
.\.venv\Scripts\python.exe server.py
```
Abrir: `http://127.0.0.1:9120`

## UI em hot reload
```powershell
cd ui
npm run dev
```

## Testes rapidos
```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

## Lint rapido
```powershell
.\.venv\Scripts\python.exe -m ruff check core services utils tests scripts/download_sdk.py
```

## Quando gerar EXE
Gerar `PyInstaller` apenas para validacao pre-release (nao para cada alteracao).
