# Release Guide

## Versioning

WootFlow uses **Semantic Versioning** (`MAJOR.MINOR.PATCH`):

| Type | When to use |
|------|-------------|
| `PATCH` | Bug fixes, no breaking changes (e.g. `3.2.1`) |
| `MINOR` | New features, backwards compatible (e.g. `3.3.0`) |
| `MAJOR` | Breaking changes (e.g. `4.0.0`) |

## Pre-release Checklist

Run these locally before tagging:

```powershell
# 1. Tests
python -m pytest tests -q

# 2. Linter
python -m ruff check core services utils tests scripts/download_sdk.py

# 3. UI build
cd ui ; npm run build ; cd ..

# 4. Verify local installer build (optional but recommended)
powershell -ExecutionPolicy Bypass -File .\scripts\download_installer_prereqs.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\build_installer.ps1 -Version X.Y.Z
```

Update [CHANGELOG.md](../CHANGELOG.md) with the new version and date before tagging.

## Creating a Release

```powershell
# Tag the release
git tag vX.Y.Z
git push origin vX.Y.Z
```

GitHub Actions ([release.yml](../.github/workflows/release.yml)) automatically:

1. Sets `APP_VERSION` from the tag
2. Builds the React UI
3. Packages the Python app into a standalone EXE via PyInstaller
4. Builds the Windows installer via Inno Setup
5. Creates a GitHub Release with:
   - `WootFlow-vX.Y.Z-win-portable.zip` — no installation needed, extract and run
   - `WootFlow-Setup-vX.Y.Z-win.exe` — standard Windows installer
   - Auto-generated release notes from merged PRs and commits

## Release Asset Naming

| File | Description |
|------|-------------|
| `WootFlow-vX.Y.Z-win-portable.zip` | Portable build — extract anywhere and run `WootFlow.exe` |
| `WootFlow-Setup-vX.Y.Z-win.exe` | Installer — recommended for most users |

## Hotfix / Patch Releases

For urgent fixes on the current version:

```powershell
git checkout main
# apply fix, commit
git tag v3.2.2
git push origin v3.2.2
```

## CI on Pull Requests

Every PR and push to `main` runs the [CI workflow](../.github/workflows/ci.yml):
- Lint (Ruff)
- Tests (pytest)

Releases are only triggered by `v*` tags.

