# WootFlow

Aplicacao desktop para controlar iluminacao RGB do teclado Wooting.

## Inicio rapido

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_all.ps1
.\.venv\Scripts\python.exe main_desktop.py
```

## Fluxo profissional recomendado

- Desenvolvimento sem rebuild de EXE: ver [docs/dev.md](docs/dev.md)
- Release e versionamento SemVer: ver [docs/release.md](docs/release.md)
- Arquitetura e migracao: ver [docs/architecture.md](docs/architecture.md) e [docs/migration_plan.md](docs/migration_plan.md)

## Build local (apenas quando necessario)

```powershell
cd ui
npm run build
cd ..
.\.venv\Scripts\python.exe -m PyInstaller WootingRGB.spec --clean -y
```

## Instalador

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_installer_prereqs.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\build_installer.ps1 -Version X.Y.Z
```

## CI/CD

- PR / push main: [ci.yml](.github/workflows/ci.yml) (lint + testes)
- Tag `v*`: [release.yml](.github/workflows/release.yml) (build + release)
