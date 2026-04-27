# Release Workflow

## Versionamento
Este projeto usa **SemVer**: `MAJOR.MINOR.PATCH`.

- PATCH: bugfix sem quebra
- MINOR: feature compativel
- MAJOR: mudanca com quebra

## Checklist local
1. Testes: `python -m pytest tests -q`
2. Lint: `python -m ruff check core services utils tests scripts/download_sdk.py`
3. Build UI: `cd ui ; npm run build`

## Build local de instalador
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_installer_prereqs.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\build_installer.ps1 -Version X.Y.Z
```

## Release oficial (GitHub Actions)
1. Criar tag:
```powershell
git tag vX.Y.Z
git push origin vX.Y.Z
```
2. O workflow [release.yml](../.github/workflows/release.yml) publica:
- zip portatil
- instalador Windows
- release notes automaticas

## Estrategia de CI
- PR: lint + testes (workflow [ci.yml](../.github/workflows/ci.yml))
- Tag `v*`: build + release
