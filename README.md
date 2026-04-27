# WootFlow

Aplicacao desktop para controlar iluminacao RGB do teclado Wooting.

## Inicio rapido

```powershell
powershell -ExecutionPolicy Bypass -File .\run_app.ps1
```

Este comando faz o fluxo completo para desenvolvimento local:

1. verifica e instala dependencias Python/UI
2. gera build da UI se necessario
3. abre a aplicacao desktop

Opcoes uteis:

```powershell
# Forcar rebuild da UI
powershell -ExecutionPolicy Bypass -File .\run_app.ps1 -ForceUiBuild

# Ignorar build da UI
powershell -ExecutionPolicy Bypass -File .\run_app.ps1 -SkipUiBuild
```

## Fluxo profissional recomendado

- Desenvolvimento sem rebuild de EXE: ver [docs/dev.md](docs/dev.md)
- Release e versionamento SemVer: ver [docs/release.md](docs/release.md)
- Arquitetura e migracao: ver [docs/architecture.md](docs/architecture.md) e [docs/migration_plan.md](docs/migration_plan.md)
- Publicacao profissional no GitHub: ver [docs/github_publish_checklist.md](docs/github_publish_checklist.md)

## Build local (apenas quando necessario)

```powershell
cd ui
npm run build
cd ..
.\.venv\Scripts\python.exe -m PyInstaller WootingRGB.spec --clean -y --workpath .\.artifacts\pyinstaller\work --distpath .\dist
```

Notas sobre artefactos:

- `dist/WootingRGB/` = output final portable (usar para testes e installer).
- `.artifacts/pyinstaller/work/` = temporario do PyInstaller (intermedio, pode apagar).
- `build/` antigo ja nao e usado pelo script `scripts/build_installer.ps1`.

## Instalador

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_installer_prereqs.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\build_installer.ps1 -Version X.Y.Z
```

Se quiseres limpar tudo antes de recomecar um build:

```powershell
Remove-Item -Recurse -Force .\dist\WootingRGB, .\.artifacts\pyinstaller\work, .\build -ErrorAction SilentlyContinue
```

## CI/CD

- PR / push main: [ci.yml](.github/workflows/ci.yml) (lint + testes)
- Tag `v*`: [release.yml](.github/workflows/release.yml) (build + release)

## Git hygiene (importante)

- Sim: `gitignore` e o mecanismo certo para impedir novos ficheiros temporarios/build de entrarem no repo.
- Nao: `gitignore` nao remove ficheiros que ja estao rastreados.
- Para parar de rastrear um ficheiro ja comitado, usa:

```powershell
git rm --cached <ficheiro>
git commit -m "stop tracking generated file"
```
